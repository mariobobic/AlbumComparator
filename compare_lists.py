def load_list(path):
    with open(path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

# Replace with your actual filenames
local_file = 'OnePlus_8_Pro_local_list.txt'
google_file = 'OnePlus_8_Pro_google_list.txt'

print("📂 Loading file lists...")
local_items = load_list(local_file)
google_items = load_list(google_file)

only_local = local_items - google_items        # In local but not in Google Photos
only_google = google_items - local_items       # In Google Photos but not local
matched = local_items & google_items           # In both

print("\n🔍 Comparison Summary:")
print(f"✅ Matched items: {len(matched)}")
print(f"❌ Missing in Google Photos (only in local): {len(only_local)}")
print(f"📤 Missing locally (only in Google Photos): {len(only_google)}")

# Print the actual differences
if only_local:
    print("\n❌ Files missing in Google Photos:")
    for name in sorted(only_local):
        print(f"  - {name}")

if only_google:
    print("\n📤 Files missing locally (only in Google Photos):")
    for name in sorted(only_google):
        print(f"  - {name}")

if not only_local and not only_google:
    print("\n🎉 Perfect match! No differences found.")
