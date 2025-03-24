import os
import pickle
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
ALBUM_NAME = 'OnePlus 8 Pro'  # Change to your desired album name

def authenticate():
    print("🔐 Authenticating with Google...")
    creds = None
    if os.path.exists('token.pickle'):
        print("🔄 Loading saved credentials...")
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("♻️ Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🌐 Starting OAuth2 flow. A browser window will open...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print("✅ Authenticated successfully.")
    return creds

def get_album_id(access_token, album_name):
    print(f"🔍 Searching for album: {album_name}")
    url = 'https://photoslibrary.googleapis.com/v1/albums'
    headers = {'Authorization': f'Bearer {access_token}'}
    albums = []

    next_page_token = ''
    page = 1
    while True:
        print(f"📄 Fetching albums page {page}...")
        params = {'pageSize': 50}
        if next_page_token:
            params['pageToken'] = next_page_token
        response = requests.get(url, headers=headers, params=params).json()
        albums.extend(response.get('albums', []))
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        page += 1

    for album in albums:
        print(f"🔗 Found album: {album.get('title')}")
        if album.get('title') == album_name:
            print(f"🎯 Album matched: {album_name}")
            return album['id']
    print(f"❌ Album '{album_name}' not found.")
    return None

def get_album_filenames(access_token, album_id):
    print(f"📥 Fetching media items from album...")
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
    headers = {'Authorization': f'Bearer {access_token}'}
    filenames = []

    next_page_token = ''
    batch = 1
    total = 0

    while True:
        print(f"📦 Fetching batch {batch}...")
        body = {
            'albumId': album_id,
            'pageSize': 100
        }
        if next_page_token:
            body['pageToken'] = next_page_token

        response = requests.post(url, headers=headers, json=body).json()

        media_items = response.get('mediaItems', [])
        filenames_batch = [item['filename'] for item in media_items]
        filenames.extend(filenames_batch)
        total += len(filenames_batch)

        print(f"   ➕ Added {len(filenames_batch)} items (total: {total})")

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        batch += 1

    print(f"✅ Finished fetching. Total items: {len(filenames)}")
    return filenames

def main():
    creds = authenticate()
    access_token = creds.token

    print(f"\n🚀 Starting export for album: {ALBUM_NAME}")
    album_id = get_album_id(access_token, ALBUM_NAME)
    if not album_id:
        return

    filenames = get_album_filenames(access_token, album_id)

    output_file = f'{ALBUM_NAME.replace(" ", "_")}_google_list.txt'
    print(f"💾 Saving filenames to: {output_file}")
    with open(output_file, 'w') as f:
        for name in filenames:
            f.write(name + '\n')
    print("🎉 Done!")

if __name__ == '__main__':
    main()
