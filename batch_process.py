import os
from google_photos_exporter import GooglePhotosFilenameExporter
from ssh_exporter import SshFilenameExporter
from local_exporter import LocalFilenameExporter
from compare import compare_filenames
from utils import strip_date_prefix

EXPORT_DIR = './exported'

EXPORTER_MAP = {
    'google': GooglePhotosFilenameExporter,
    'ssh': SshFilenameExporter,
    'local': LocalFilenameExporter
}

def process_batch(albums: list, source1: str, source2: str):
    exporter1 = EXPORTER_MAP[source1]()
    exporter2 = EXPORTER_MAP[source2]()

    for album in albums:
        album_name = strip_date_prefix(album)
        safe_name = album_name.replace(' ', '_')
        file1 = os.path.join(EXPORT_DIR, f"{safe_name}_list_{source1}.txt")
        file2 = os.path.join(EXPORT_DIR, f"{safe_name}_list_{source2}.txt")

        print(f"\n🚀 Processing album: {album_name}")
        exporter1.export_filenames(album, file1)
        exporter2.export_filenames(album, file2)

        compare_filenames(file1, file2, source1, source2)

def discover_remote_albums() -> list[str]:
    ssh_exporter = SshFilenameExporter()
    print("🔐 Connecting to SSH host to fetch album list...")
    client = ssh_exporter._connect()
    stdin, stdout, stderr = client.exec_command(f"ls '{ssh_exporter.remote_root}'")
    folders = sorted(stdout.read().decode().splitlines())
    client.close()

    return folders

def discover_local_albums() -> list[str]:
    local_exporter = LocalFilenameExporter()
    folders = sorted([f for f in os.listdir(local_exporter.root_directory)
                      if os.path.isdir(os.path.join(local_exporter.root_directory, f))])

    return folders