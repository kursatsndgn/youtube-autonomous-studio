"""
Voice Generation & Faster-Whisper Alignment Engine
Powered by OpenVoice / Edge-TTS and SYSTRAN/faster-whisper.
"""

import asyncio
import json
import os
from typing import Dict, List, Any


class VoiceEngine:
    def __init__(self, output_dir: str = "output", voice: str = "tr-TR-AhmetNeural"):
        self.output_dir = output_dir
        self.voice = voice
        os.makedirs(output_dir, exist_ok=True)

    async def generate_tts(self, text: str, output_wav: str) -> str:
        """Edge-TTS kullanarak yüksek kaliteli ses dosyası üretir."""
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, self.voice, rate="+5%")
            await communicate.save(output_wav)
            print(f"[+] TTS sesi üretildi: {output_wav}")
            return output_wav
        except ImportError:
            print("[!] edge-tts yüklü değil. Simüle ses oluşturuluyor.")
            # Boş dosya simülasyonu
            with open(output_wav, "wb") as f:
                f.write(b"SIMULATED_AUDIO_CONTENT")
            return output_wav

    def align_words_faster_whisper(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Faster-Whisper ile kelime bazlı timestamp çıkarır.
        """
        try:
            from faster_whisper import WhisperModel
            print("[*] Faster-Whisper modeli yükleniyor...")
            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path, word_timestamps=True)

            words_data = []
            for segment in segments:
                for word in segment.words:
                    words_data.append({
                        "word": word.word.strip(),
                        "start": round(word.start, 2),
                        "end": round(word.end, 2),
                        "probability": round(word.probability, 2)
                    })

            align_path = os.path.join(self.output_dir, "word_alignment.json")
            with open(align_path, "w", encoding="utf-8") as f:
                json.dump(words_data, f, indent=2, ensure_ascii=False)
            print(f"[+] Kelime hizalaması tamamlandı: {align_path} ({len(words_data)} kelime)")
            return words_data

        except ImportError:
            print("[!] faster-whisper kütüphanesi bulunamadı. Heuristic zamanlama kullanılıyor.")
            # Fallback heuristic
            words_data = [
                {"word": "Bu", "start": 0.0, "end": 0.4},
                {"word": "video", "start": 0.4, "end": 0.9},
                {"word": "otonom", "start": 0.9, "end": 1.5},
                {"word": "üretildi", "start": 1.5, "end": 2.2}
            ]
            align_path = os.path.join(self.output_dir, "word_alignment.json")
            with open(align_path, "w", encoding="utf-8") as f:
                json.dump(words_data, f, indent=2, ensure_ascii=False)
            return words_data
