import os
import paramiko
from interfaces import FilenameExporter
from config_loader import load_config
from utils import strip_date_prefix
from utils import write_sorted_file

class SshFilenameExporter(FilenameExporter):
    def __init__(self):
        config = load_config('ssh_config.json')
        self.host = config['host']
        self.username = config['username']
        self.password = config['password']
        self.port = config.get('port', 22)
        self.remote_root = os.path.expanduser(config['remote_root'])

    def _connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, port=self.port, username=self.username, password=self.password)
        return client

    def export_filenames(self, album_name: str, output_path: str) -> None:
        album_name = strip_date_prefix(album_name)
        print(f"🔐 Connecting to SSH host {self.host}:{self.port}...")
        client = self._connect()

        stdin, stdout, stderr = client.exec_command(f"ls '{self.remote_root}'")
        folders = stdout.read().decode().splitlines()
        folder = next((f for f in folders if f.endswith(album_name)), None)
        if not folder:
            raise FileNotFoundError(f"Album folder ending with '{album_name}' not found on remote")

        full_path = os.path.join(self.remote_root, folder)
        print(f"📁 Reading remote files from: {full_path}")
        stdin, stdout, stderr = client.exec_command(f"ls -p '{full_path}'")
        filenames = [
            line for line in stdout.read().decode().splitlines()
            if not line.endswith('/')
        ]

        write_sorted_file(output_path, filenames)

        print(f"💾 Exported {len(filenames)} remote filenames to {output_path}")
        client.close()
