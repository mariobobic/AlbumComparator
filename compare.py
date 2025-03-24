def compare_filenames(file1: str, file2: str, source1: str, source2: str):
    def load_list(path):
        with open(path, 'r') as f:
            return set(line.strip() for line in f if line.strip())

    print("📂 Loading file lists...")
    items1 = load_list(file1)
    items2 = load_list(file2)

    only_in_1 = items1 - items2
    only_in_2 = items2 - items1
    matched = items1 & items2

    print("\n🔍 Comparison Summary:")
    print(f"✅ Matched items: {len(matched)}")
    print(f"❌ Missing in {source2} (only in {source1}): {len(only_in_1)}")
    print(f"📤 Missing in {source1} (only in {source2}): {len(only_in_2)}")

    if only_in_1:
        print(f"\n❌ Files missing in {source2}:")
        for name in sorted(only_in_1):
            print(f"  - {name}")

    if only_in_2:
        print(f"\n📤 Files missing in {source1}:")
        for name in sorted(only_in_2):
            print(f"  - {name}")

    print(f"--------------------------------------------------")
