import os
import requests
from auth import authenticate
from interfaces import FilenameExporter
from utils import strip_date_prefix
from utils import write_sorted_file

class GooglePhotosFilenameExporter(FilenameExporter):
    def __init__(self):
        self.access_token = authenticate().token
        self.album_map = {}
        self._albums_fully_loaded = False
        self._current_page = 1
        self._next_page_token = ''

    def get_album_id(self, album_name):
        print(f"🔍 Searching for album: {album_name}")

        if album_name in self.album_map:
            print(f"✅ Album found in cache: {album_name}")
            return self.album_map[album_name]

        url = 'https://photoslibrary.googleapis.com/v1/albums'
        headers = {'Authorization': f'Bearer {self.access_token}'}

        while not self._albums_fully_loaded:
            print(f"📄 Fetching albums page {self._current_page}...")
            params = {'pageSize': 50}
            if self._next_page_token:
                params['pageToken'] = self._next_page_token

            response = requests.get(url, headers=headers, params=params).json()
            albums = response.get('albums', [])
            for album in albums:
                title = album.get('title')
                if title and title not in self.album_map:
                    self.album_map[title] = album['id']

            self._next_page_token = response.get('nextPageToken')
            if not self._next_page_token:
                self._albums_fully_loaded = True

            if album_name in self.album_map:
                print(f"✅ Album matched: {album_name}")
                return self.album_map[album_name]

            self._current_page += 1

        print(f"⚠️ Album not found: {album_name}")
        return None

    def get_album_filenames(self, album_id):
        print(f"📥 Fetching media items from album ID: {album_id}")
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        filenames = []

        next_page_token = ''
        batch = 1
        while True:
            print(f"📦 Fetching batch {batch}...")
            body = {'albumId': album_id, 'pageSize': 100}
            if next_page_token:
                body['pageToken'] = next_page_token

            response = requests.post(url, headers=headers, json=body).json()
            media_items = response.get('mediaItems', [])
            filenames_batch = [item['filename'] for item in media_items]
            filenames.extend(filenames_batch)
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
            batch += 1

        print(f"✅ Finished fetching {len(filenames)} items.")
        return filenames

    def export_filenames(self, album_name: str, output_path: str) -> None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        album_name = strip_date_prefix(album_name)
        album_id = self.get_album_id(album_name)

        if not album_id:
            print(f"⚠️ Skipping export for missing album: {album_name}")
            return

        filenames = self.get_album_filenames(album_id)
        write_sorted_file(output_path, filenames)
        print(f"💾 Exported {len(filenames)} filenames to {output_path}")
