import os
from interfaces import FilenameExporter
from config_loader import load_config
from utils import strip_date_prefix
from utils import write_sorted_file

class LocalFilenameExporter(FilenameExporter):
    def __init__(self):
        config = load_config('local_config.json')
        self.root_directory = os.path.expanduser(config['root_directory'])

    def export_filenames(self, album_name: str, output_path: str) -> None:
        album_name = strip_date_prefix(album_name)
        folder = next((f for f in os.listdir(self.root_directory)
                      if f.endswith(album_name)), None)
        if not folder:
            raise FileNotFoundError(f"Album folder ending with '{album_name}' not found in {self.root_directory}")

        folder_path = os.path.join(self.root_directory, folder)
        print(f"📁 Reading local files from: {folder_path}")
        filenames = [
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
        write_sorted_file(output_path, filenames)
        print(f"💾 Exported {len(filenames)} filenames to {output_path}")
