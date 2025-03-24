import os

def write_sorted_file(output_path: str, items: list[str]):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        for name in sorted(items):
            f.write(name + '\n')

def strip_date_prefix(album_name: str) -> str:
    """
    Removes 'YYYY-MM-DD ' prefix from album/folder names if it exists.
    Returns just the device name.
    """
    return album_name.split(' ', 1)[-1]
