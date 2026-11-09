"""
YouTube Data API v3 Resumable Uploader
Handles automated publishing of long-form videos and 9:16 Shorts via YouTube Data API v3.
"""

import os
import sys
import time
from typing import List, Optional, Dict, Any


class YouTubeUploader:
    def __init__(self, client_secrets: str = "config/client_secrets.json", token_path: str = "config/token.pickle"):
        self.client_secrets = client_secrets
        self.token_path = token_path
        self.service = None

    def authenticate(self):
        """Google OAuth2 akışını başlatır ve yetki alır."""
        try:
            import pickle
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = [
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube"
            ]

            credentials = None
            if os.path.exists(self.token_path):
                with open(self.token_path, "rb") as token:
                    credentials = pickle.load(token)

            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                elif os.path.exists(self.client_secrets):
                    flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets, SCOPES)
                    credentials = flow.run_local_server(port=0)
                    with open(self.token_path, "wb") as token:
                        pickle.dump(credentials, token)
                else:
                    raise FileNotFoundError(f"{self.client_secrets} bulunamadı; YouTube OAuth istemcisi gerekli.")

            self.service = build("youtube", "v3", credentials=credentials)
            print("[+] YouTube API yetkilendirmesi başarılı!")
            return self.service
        except Exception as e:
            raise RuntimeError(f"YouTube yetkilendirme hatası: {e}") from e

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        category_id: str = "28",
        privacy_status: str = "unlisted",
        is_shorts: bool = False,
        thumbnail_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Videoyu YouTube'a yükler (Long-form veya #Shorts)."""
        tags = tags or ["tarih", "futbol", "belgesel", "hikaye"]
        if is_shorts and "#shorts" not in title.lower():
            title = f"{title} #Shorts"
            if "#shorts" not in description.lower():
                description = f"{description}\n\n#Shorts"

        print(f"\n[*] 📡 YouTube'a Yükleniyor: {title}")
        print(f"    - Dosya: {video_path}")
        print(f"    - Tür: {'YouTube Shorts' if is_shorts else 'Ana video'}")
        print(f"    - Gizlilik: {privacy_status}")

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video bulunamadı: {video_path}")

        # Eğer API yetkilendirmesi hazırsa gerçek upload yap
        if not self.service:
            self.authenticate()

        if self.service:
            try:
                from googleapiclient.http import MediaFileUpload
                body = {
                    "snippet": {
                        "title": title[:100],
                        "description": description[:5000],
                        "tags": tags,
                        "categoryId": category_id
                    },
                    "status": {
                        "privacyStatus": privacy_status,
                        "selfDeclaredMadeForKids": False
                    }
                }
                media = MediaFileUpload(video_path, chunksize=1024*1024*4, resumable=True, mimetype="video/mp4")
                request = self.service.videos().insert(part="snippet,status", body=body, media_body=media)

                response = None
                print("[*] Yükleme başlatıldı...")
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        print(f"    Yükleniyor: %{int(status.progress() * 100)}")

                video_id = response.get("id")
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"[+] Başarıyla yüklendi! Link: {video_url}")

                # Thumbnail yükleme (sadece uzun videolarda)
                if thumbnail_path and os.path.exists(thumbnail_path) and not is_shorts:
                    try:
                        self.service.thumbnails().set(
                            videoId=video_id,
                            media_body=MediaFileUpload(thumbnail_path)
                        ).execute()
                        print("[+] Thumbnail yüklendi!")
                    except Exception as te:
                        print(f"[!] Thumbnail yükleme uyarısı: {te}")

                return {"status": "success", "video_id": video_id, "url": video_url}
            except Exception as e:
                raise RuntimeError(f"YouTube yükleme başarısız: {e}") from e
        raise RuntimeError("YouTube servisi hazır değil; yükleme yapılmadı.")
