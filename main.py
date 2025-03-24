import argparse
from batch_process import process_batch, discover_remote_albums
from config_loader import load_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare photo album filenames between sources.")
    parser.add_argument('--source1', required=True, choices=['google', 'ssh', 'local'])
    parser.add_argument('--source2', required=True, choices=['google', 'ssh', 'local'])
    parser.add_argument('--exclude', nargs='*', default=[], help='Folder names to exclude from processing')
    args = parser.parse_args()

    ssh_config = load_config('ssh_config.json')
    print(f"📁 Looking for folders in remote SSH directory: {ssh_config['remote_root']}")
    folders = discover_remote_albums(excluded=args.exclude)

    if folders:
        process_batch(folders, source1=args.source1, source2=args.source2)
    else:
        print("⚠️ No albums to process.")
