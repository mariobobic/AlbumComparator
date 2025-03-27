import argparse
from batch_process import process_batch, discover_remote_albums, discover_local_albums
from config_loader import load_config

def get_folders_from_source(args) -> list[str]:
    if args.source1 == 'ssh':
        ssh_config = load_config('ssh_config.json')
        print(f"📁 Looking for folders in remote SSH directory: {ssh_config['remote_root']}")
        return discover_remote_albums()
    elif args.source1 == 'local':
        local_config = load_config('local_config.json')
        print(f"📁 Looking for folders in local directory: {local_config['root_directory']}")
        return discover_local_albums()
    else:
        print("❌ Invalid source1: Only 'ssh' or 'local' can be used to discover folders.")
    exit(1)

def apply_exclusions(folders: list[str], excluded: list[str]) -> list[str]:
    applied_exclusions = [f for f in excluded if f in folders]
    if applied_exclusions:
        print(f"🚫 Excluding folders: {applied_exclusions}")
        return [f for f in folders if f not in applied_exclusions]
    return folders

def confirm_folders(folders: list[str]):
    print("📦 Found folders:")
    for f in folders:
        print(f"  - {f}")

    confirm = input("❓ Use these folders? [y/N]: ")
    if confirm.lower() != 'y':
        print("❌ Aborted.")
        exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare photo album filenames between sources.")
    parser.add_argument('--source1', required=True, choices=['google', 'ssh', 'local'])
    parser.add_argument('--source2', required=True, choices=['google', 'ssh', 'local'])
    parser.add_argument('--exclude', nargs='*', default=[], help='Folder names to exclude from processing')
    args = parser.parse_args()

    folders = get_folders_from_source(args)
    folders = apply_exclusions(folders, args.exclude)
    confirm_folders(folders)

    if folders:
        process_batch(folders, source1=args.source1, source2=args.source2)
    else:
        print("⚠️ No albums to process.")
