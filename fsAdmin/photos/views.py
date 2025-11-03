import os
import time
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

# --- Настройки ---
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'service_account.json'
ROOT_FOLDER_ID = '1krbXYK0r-jzotuqf-7tOMsXqA8IX1qvX'
CACHE_TIMEOUT = 60 * 60  # 1 час
MEDIA_FOLDER = os.path.join(settings.MEDIA_ROOT, "albums")  # локална папка за снимките

# --- Утилити функции ---
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def download_image_if_not_exists(file_id, filename, album_name):
    """Сваля снимка локално, ако още я няма"""
    album_dir = os.path.join(MEDIA_FOLDER, album_name)
    os.makedirs(album_dir, exist_ok=True)
    file_path = os.path.join(album_dir, filename)

    if os.path.exists(file_path):
        return os.path.join("albums", album_name, filename)  # относителен път (MEDIA_URL + ...)

    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        return os.path.join("albums", album_name, filename)
    else:
        print(f"⚠️ Неуспешно теглене: {filename}")
        return None


# --- API изгледи ---
class AlbumsView(APIView):
    """Връща списък с албуми и техните cover изображения"""
    def get(self, request):
        cached = cache.get("albums_list")
        if cached:
            print("⚡ Връщам кеширан списък")
            return Response(cached)

        service = get_drive_service()
        albums_result = service.files().list(
            q=f"'{ROOT_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id, name)"
        ).execute()

        albums = albums_result.get('files', [])
        album_list = []

        for album in albums:
            images_result = service.files().list(
                q=f"'{album['id']}' in parents and mimeType contains 'image/' and trashed=false",
                fields="files(id, name)",
                orderBy="createdTime desc"
            ).execute()
            images = images_result.get('files', [])
            if not images:
                continue

            # теглим първата снимка за cover
            first_img = images[0]
            local_path = download_image_if_not_exists(first_img['id'], first_img['name'], album['name'])
            cover_url = request.build_absolute_uri(settings.MEDIA_URL + local_path) if local_path else None

            album_list.append({
                "id": album["id"],
                "name": album["name"],
                "cover": cover_url,
                "count": len(images)
            })

        data = {"albums": album_list, "timestamp": int(time.time())}
        cache.set("albums_list", data, CACHE_TIMEOUT)
        return Response(data)


class AlbumDetailView(APIView):
    """Връща всички снимки от конкретен албум"""
    def get(self, request, album_id):
        cached = cache.get(f"album_{album_id}")
        if cached:
            print(f"⚡ Връщам кеш за албум {album_id}")
            return Response(cached)

        service = get_drive_service()
        images_result = service.files().list(
            q=f"'{album_id}' in parents and mimeType contains 'image/' and trashed=false",
            fields="files(id, name)"
        ).execute()

        images = images_result.get('files', [])
        urls = []
        album_name = None

        # намираме името на албума (само веднъж)
        folder_info = service.files().get(fileId=album_id, fields="name").execute()
        album_name = folder_info["name"]

        for img in images:
            local_path = download_image_if_not_exists(img['id'], img['name'], album_name)
            if local_path:
                urls.append({
                    "name": img["name"],
                    "url": request.build_absolute_uri(settings.MEDIA_URL + local_path)
                })

        data = {"album_id": album_id, "images": urls}
        cache.set(f"album_{album_id}", data, CACHE_TIMEOUT)
        return Response(data)
