"""
Voice Pipeline: Edge-TTS (Türkçe) + OpenVoice V2 ton rengi dönüştürme + kelime zamanlaması.

- generate_tts       : Edge-TTS ile ses + WordBoundary kelime zamanları (Whisper gerekmez).
- clone_tone         : OpenVoice V2 ToneColorConverter ile sesi referans tınıya dönüştürür.
                       (OpenVoice V2 Türkçe TTS yapmaz; dönüştürücü dilden bağımsızdır.)
- align_words_faster_whisper : Dış kaynaklı sesler için faster-whisper hizalaması.

Kelime formatı: {"w","s","e"} (+ geriye uyumluluk için "word","start","end").
Bağımlılık eksikse veya adım başarısızsa istisna fırlatır; sahte çıktı üretmez.
"""

import json
import os
from typing import Any, Dict, List, Optional


def _word(text: str, s: float, e: float) -> Dict[str, Any]:
    return {"w": text, "s": round(s, 3), "e": round(e, 3), "word": text, "start": round(s, 3), "end": round(e, 3)}


class VoiceEngine:
    def __init__(self, output_dir: str = "output", voice: str = "tr-TR-AhmetNeural", rate: str = "-4%",
                 openvoice_ckpt: str = "vendor/OpenVoice/checkpoints_v2",
                 reference_voice: str = "config/voice/reference.wav"):
        self.output_dir = output_dir
        self.voice = voice
        self.rate = rate
        self.openvoice_ckpt = openvoice_ckpt
        self.reference_voice = reference_voice
        self.last_words: List[Dict[str, Any]] = []
        os.makedirs(output_dir, exist_ok=True)

    # ------------------------------------------------------------------ Edge-TTS
    async def generate_tts(self, text: str, output_path: str) -> str:
        """Edge-TTS ile ses üretir; kelime zamanlarını self.last_words ve word_alignment.json'a yazar."""
        import edge_tts  # yoksa ImportError -> pipeline durur

        words: List[Dict[str, Any]] = []
        com = edge_tts.Communicate(text, self.voice, rate=self.rate, boundary="WordBoundary")
        with open(output_path, "wb") as f:
            async for chunk in com.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    s = chunk["offset"] / 1e7
                    words.append(_word(chunk["text"], s, s + chunk["duration"] / 1e7))
        if not words or os.path.getsize(output_path) == 0:
            raise RuntimeError("Edge-TTS boş çıktı döndürdü.")
        self.last_words = words
        self._save_alignment(words)
        print(f"[+] TTS üretildi: {output_path} ({len(words)} kelime)")
        return output_path

    # ------------------------------------------------------------------ OpenVoice
    def clone_tone(self, source_audio: str, output_wav: str, reference: Optional[str] = None,
                   device: Optional[str] = None) -> str:
        """OpenVoice V2 ile source_audio'yu referans sesin tınısına dönüştürür."""
        reference = reference or self.reference_voice
        if not os.path.isfile(reference):
            raise FileNotFoundError(f"Referans ses yok: {reference} (10–30 sn temiz kayıt koy).")
        conv_dir = os.path.join(self.openvoice_ckpt, "converter")
        if not os.path.isfile(os.path.join(conv_dir, "checkpoint.pth")):
            raise FileNotFoundError(f"OpenVoice V2 checkpoint bulunamadı: {conv_dir} (kurulum: python scripts/install_openvoice.py).")
        try:
            import torch
            from openvoice import se_extractor
            from openvoice.api import ToneColorConverter
        except ImportError as e:
            raise ImportError("OpenVoice kurulu değil: python scripts/install_openvoice.py") from e

        device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        conv = ToneColorConverter(os.path.join(conv_dir, "config.json"), device=device)
        conv.load_ckpt(os.path.join(conv_dir, "checkpoint.pth"))
        tgt_se, _ = se_extractor.get_se(reference, conv, vad=True)
        src_se, _ = se_extractor.get_se(source_audio, conv, vad=True)
        conv.convert(audio_src_path=source_audio, src_se=src_se, tgt_se=tgt_se,
                     output_path=output_wav, message="@MyShell")
        print(f"[+] OpenVoice ton dönüştürme tamam: {output_wav}")
        return output_wav

    # ------------------------------------------------------------------ Whisper
    def align_words_faster_whisper(self, audio_path: str, model_size: str = "small",
                                   language: str = "tr") -> List[Dict[str, Any]]:
        """Dış kaynaklı ses için kelime zamanları. Edge-TTS sesi için self.last_words zaten doğru."""
        from faster_whisper import WhisperModel  # yoksa ImportError -> pipeline durur

        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, word_timestamps=True, language=language)
        words = [_word(w.word.strip(), w.start, w.end) for seg in segments for w in seg.words]
        if not words:
            raise RuntimeError(f"Whisper hiç kelime bulamadı: {audio_path}")
        self._save_alignment(words)
        return words

    def _save_alignment(self, words: List[Dict[str, Any]]) -> str:
        path = os.path.join(self.output_dir, "word_alignment.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(words, f, indent=2, ensure_ascii=False)
        return path
