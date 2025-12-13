#!/usr/bin/env python3
"""
Manual rename for Episode_02 videos without titles in HTML
Uses titles from Playwright extraction log
"""

import re
from pathlib import Path

# Mapping from the Playwright extraction output for Episode_02
TITLE_MAPPING = {
    101: "EnglishPod 139 - Elementary - The Weekend - Playing Chess",
    102: "EnglishPod 138 - Elementary - Daily Life - Renting A Car",
    103: "EnglishPod 137 - Upper Intermediate - Getting Internet Service",
    104: "EnglishPod 136 - Advanced - Gambling",
    105: "EnglishPod 135 - Elementary - Cheer Up",
    106: "EnglishPod 132 - Upper Intermediate - Mechanic",
    107: "EnglishPod 133 - Intermediate - Doing Laundry",
    108: "EnglishPod 131 - Intermediate - Daily Life - Buying a Suit",
    110: "EnglishPod 129 - Intermediate - New Guy in Town 8",
    111: "EnglishPod 127 - Elementary - Daily Life - Buying a Computer",
    112: "EnglishPod 123 - Intermediate - 1990's",
    113: "EnglishPod 121 - Advanced - Presidential Speech",
    114: "EnglishPod 120 - Upper Intermediate - Boxing",
    115: "EnglishPod 118 - Intermediate - Baby Talk",
    125: "EnglishPod 104 - Elementary - New Guy in Town 9",
    127: "EnglishPod 134 - Elementary - Daily Life - Asking for a Raise",
    128: "EnglishPod 130 - Intermediate - Daily Life - Buying a Car",
    129: "EnglishPod 126 - Elementary - Daily Life - Asking for Directions",
    130: "EnglishPod 125 - Intermediate - Daily Life - Renting an Apartment",
    131: "EnglishPod 124 - Elementary - Daily Life - Ordering Fast Food",
    132: "EnglishPod 122 - Intermediate - Daily Life - At the Pharmacy",
    134: "EnglishPod 119 - Elementary - Daily Life - Calling Customer Service",
    138: "EnglishPod 103 - Elementary - Baby I'm Sorry"
}


def sanitize_filename(title):
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


def rename_remaining_files():
    """Rename files that don't have titles in their HTML"""
    
    descriptions_dir = Path('youtube_descriptions/Episode_02')
    
    if not descriptions_dir.exists():
        print("❌ youtube_descriptions/Episode_02 folder not found!")
        return
    
    print("📁 Renaming Episode_02 files with manual title mapping...\n")
    
    renamed = 0
    skipped = 0
    
    for video_num, title in TITLE_MAPPING.items():
        old_filename = f"video_{video_num}.html"
        old_path = descriptions_dir / old_filename
        
        if not old_path.exists():
            print(f"⚠️  File not found: {old_filename}")
            skipped += 1
            continue
        
        # Create new filename
        safe_title = sanitize_filename(title)
        new_filename = f"video_{video_num:03d}_{safe_title}.html"
        new_path = descriptions_dir / new_filename
        
        # Rename the file
        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: {old_filename}")
            print(f"   → {new_filename}")
            renamed += 1
        except Exception as e:
            print(f"❌ Error renaming {old_filename}: {e}")
            skipped += 1
    
    # Summary
    print("\n" + "="*80)
    print("📊 RENAME SUMMARY - Episode_02")
    print("="*80)
    print(f"✅ Renamed: {renamed} files")
    print(f"⚠️  Skipped: {skipped} files")
    print(f"📁 Location: {descriptions_dir.absolute()}")
    print("="*80)
    
    # Check total files
    all_files = list(descriptions_dir.glob('video_*.html'))
    print(f"\n📊 Total files in Episode_02: {len(all_files)}")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           MANUAL RENAME - EPISODE_02                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    rename_remaining_files()
    
    print("\n✅ Done! All Episode_02 files should now have proper names.")
