import os
import requests
from datetime import datetime
from auth import authenticate
from interfaces import FilenameExporter
from pathvalidate import sanitize_filename
from utils import strip_date_prefix, write_sorted_file

class GooglePhotosFilenameExporter(FilenameExporter):
    def __init__(self):
        self.access_token = authenticate().token
        self.album_map = {}
        self._albums_fully_loaded = False
        self._current_page = 1
        self._next_page_token = ''

    def _fetch_next_album_page(self):
        url = 'https://photoslibrary.googleapis.com/v1/albums'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'pageSize': 50}

        if self._next_page_token:
            params['pageToken'] = self._next_page_token

        print(f"📄 Fetching albums page {self._current_page}...")
        response = requests.get(url, headers=headers, params=params).json()
        self._next_page_token = response.get('nextPageToken')
        if not self._next_page_token:
            self._albums_fully_loaded = True

        self._current_page += 1
        return response.get('albums', [])

    def _ensure_album_map_until(self, target_album_title):
        while not self._albums_fully_loaded:
            albums = self._fetch_next_album_page()
            for album in albums:
                title = album.get('title')
                if title and title not in self.album_map:
                    self.album_map[title] = album['id']
                if target_album_title in self.album_map:
                    break

    def get_album_id(self, album_name):
        print(f"🔍 Searching for album: {album_name}")

        if album_name in self.album_map:
            print(f"✅ Album found in cache: {album_name}")
            return self.album_map[album_name]

        self._ensure_album_map_until(album_name)

        if album_name in self.album_map:
            print(f"✅ Album matched: {album_name}")
            return self.album_map[album_name]

        print(f"⚠️ Album not found: {album_name}")
        return None

    def get_album_filenames_and_earliest_date(self, album_id):
        print(f"📥 Fetching media items from album ID: {album_id}")
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        filenames = []
        timestamps = []

        next_page_token = ''
        batch = 1
        while True:
            print(f"📦 Fetching batch {batch}...")
            body = {'albumId': album_id, 'pageSize': 100}
            if next_page_token:
                body['pageToken'] = next_page_token

            response = requests.post(url, headers=headers, json=body).json()
            media_items = response.get('mediaItems', [])

            for item in media_items:
                filenames.append(item['filename'])
                if 'mediaMetadata' in item and 'creationTime' in item['mediaMetadata']:
                    timestamps.append(datetime.fromisoformat(item['mediaMetadata']['creationTime'].replace('Z', '+00:00')))

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
            batch += 1

        earliest_date = min(timestamps) if timestamps else None
        print(f"✅ Finished fetching {len(filenames)} items.")
        return filenames, earliest_date

    def export_filenames(self, album_name: str, output_path: str) -> None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        album_name = strip_date_prefix(album_name)
        album_id = self.get_album_id(album_name)

        if not album_id:
            print(f"⚠️ Skipping export for missing album: {album_name}")
            return

        filenames, _ = self.get_album_filenames_and_earliest_date(album_id)
        write_sorted_file(output_path, filenames)
        print(f"💾 Exported {len(filenames)} filenames to {output_path}")

    def export_all_album_filenames(self, output_dir: str = './albums'):
        print("📚 Exporting filenames for all Google Photos albums...")
        os.makedirs(output_dir, exist_ok=True)

        # Ensure all albums are fetched
        self._albums_fully_loaded = False
        self._next_page_token = ''
        self._current_page = 1
        self.album_map.clear()

        while not self._albums_fully_loaded:
            albums = self._fetch_next_album_page()

            for album in albums:
                title = album['title']
                album_id = album['id']
                print(f"\n🎞️ Album: {title}")

                filenames, earliest_date = self.get_album_filenames_and_earliest_date(album_id)
                if not filenames:
                    print(f"⚠️ Skipping empty album: {title}")
                    continue

                date_prefix = earliest_date.strftime('%Y-%m-%d') if earliest_date else '0000-00-00'
                safe_title = sanitize_filename(title)
                filename = f"{date_prefix} {safe_title}.txt"
                output_path = os.path.join(output_dir, filename)

                write_sorted_file(output_path, filenames)
                print(f"💾 Exported {len(filenames)} filenames to {output_path}")
