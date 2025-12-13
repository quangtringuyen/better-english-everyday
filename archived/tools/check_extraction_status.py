#!/usr/bin/env python3
"""
Check all extracted playlists and identify missing videos
"""

from pathlib import Path
import re

def check_folder(folder_name, expected_count, start_num=1):
    """Check a folder for missing videos"""
    folder_path = Path(f"youtube_descriptions/{folder_name}")
    
    if not folder_path.exists():
        print(f"\n❌ {folder_name}: Folder doesn't exist")
        return []
    
    # Get all HTML files
    files = list(folder_path.glob("video_*.html"))
    
    # Extract video numbers
    extracted_numbers = set()
    for file in files:
        match = re.search(r'video_(\d+)', file.name)
        if match:
            extracted_numbers.add(int(match.group(1)))
    
    # Find missing
    expected_numbers = set(range(start_num, start_num + expected_count))
    missing = sorted(expected_numbers - extracted_numbers)
    
    print(f"\n📁 {folder_name}:")
    print(f"   Expected: {expected_count} videos")
    print(f"   Found: {len(extracted_numbers)} videos")
    print(f"   Missing: {len(missing)} videos")
    
    if missing:
        print(f"   Missing numbers: {missing[:20]}")  # Show first 20
        if len(missing) > 20:
            print(f"   ... and {len(missing) - 20} more")
    else:
        print(f"   ✅ Complete!")
    
    return missing


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   EXTRACTION STATUS CHECK                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    all_missing = {}
    
    # Check each folder
    all_missing['Episode_01'] = check_folder('Episode_01', 100, 1)
    all_missing['Episode_02'] = check_folder('Episode_02', 39, 101)
    all_missing['Episode_03'] = check_folder('Episode_03', 63, 140)
    all_missing['Elementary'] = check_folder('Elementary', 41, 1)
    all_missing['Intermediate'] = check_folder('Intermediate', 37, 1)
    all_missing['Upper_Intermediate'] = check_folder('Upper_Intermediate', 13, 1)
    all_missing['Advanced'] = check_folder('Advanced', 9, 1)
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    
    total_expected = 100 + 39 + 63 + 41 + 37 + 13 + 9
    total_missing = sum(len(m) for m in all_missing.values())
    total_found = total_expected - total_missing
    
    print(f"\n📈 Total Expected: {total_expected} videos")
    print(f"✅ Total Found: {total_found} videos")
    print(f"❌ Total Missing: {total_missing} videos")
    print(f"📊 Completion: {(total_found/total_expected)*100:.1f}%")
    
    # Folders needing retry
    print("\n🔄 Folders needing retry:")
    for folder, missing in all_missing.items():
        if missing:
            print(f"   - {folder}: {len(missing)} missing videos")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    main()
