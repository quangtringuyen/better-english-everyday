#!/usr/bin/env python3
"""
Manual rename for videos without titles in HTML

This script uses the titles captured during Playwright extraction
to rename the remaining files.
"""

import re
from pathlib import Path

# Mapping from the Playwright extraction output
TITLE_MAPPING = {
    54: "EnglishPod 54 - Intermediate - I'm sorry I love you 5",
    81: "EnglishPod 81 - Intermediate - Buying Underwear 2",
    83: "EnglishPod 83 - Upper Intermediate - New Guy in Town 6",
    84: "EnglishPod 84 - Intermediate - New Guy in Town 7",
    85: "EnglishPod 85 - Advanced - Drugs",
    86: "EnglishPod 86 - Intermediate - Daily Life - Applying for a Passport",
    87: "EnglishPod 087 - Elementary - Star Trek The Lost Generation",
    88: "EnglishPod 88 - Elementary - Asking for a Raise",
    89: "EnglishPod 89 - Intermediate - Skiing",
    91: "EnglishPod 91 - Advanced - Investing your Money",
    93: "EnglishPod 93 - Intermediate - Bad news",
    94: "EnglishPod 94 - Upper Intermediate - Silence please 2",
    95: "EnglishPod 095 - Intermediate - Talking About a Past Event",
    96: "EnglishPod 096 - Intermediate - 1960's English",
    97: "EnglishPod 097 - Upper Intermediate - Weather Forecast",
    98: "EnglishPod 098 - Intermediate - Flattering",
    99: "EnglishPod 099 - Advanced - Movie Review",
    100: "EnglishPod 100 - Intermediate - Where are you from"
}


def sanitize_filename(title):
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


def rename_remaining_files():
    """Rename files that don't have titles in their HTML"""
    
    descriptions_dir = Path('youtube_descriptions')
    
    if not descriptions_dir.exists():
        print("❌ youtube_descriptions folder not found!")
        return
    
    print("📁 Renaming files with manual title mapping...\n")
    
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
    print("📊 RENAME SUMMARY")
    print("="*80)
    print(f"✅ Renamed: {renamed} files")
    print(f"⚠️  Skipped: {skipped} files")
    print(f"📁 Location: {descriptions_dir.absolute()}")
    print("="*80)
    
    # Check total files
    all_files = list(descriptions_dir.glob('video_*.html'))
    print(f"\n📊 Total files in directory: {len(all_files)}")
    
    # Check for missing episodes
    missing = []
    for i in range(1, 101):
        matching_files = list(descriptions_dir.glob(f'video_{i:03d}_*.html'))
        if not matching_files:
            # Check old format
            old_format = descriptions_dir / f'video_{i}.html'
            if not old_format.exists():
                missing.append(i)
    
    if missing:
        print(f"\n⚠️  Missing episodes: {missing}")
    else:
        print(f"\n✅ All 100 episodes accounted for!")


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   MANUAL FILE RENAMER                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    rename_remaining_files()
    
    print("\n✅ Done! All files should now have proper names.")
