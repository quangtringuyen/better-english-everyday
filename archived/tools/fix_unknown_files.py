#!/usr/bin/env python3
"""
Fix Unknown files - Move them to correct level folders based on filename
"""

import re
from pathlib import Path
import shutil


def get_level_from_filename(filename):
    """Extract level from filename"""
    filename_lower = filename.lower()
    
    if 'elementary' in filename_lower:
        return 'Elementary'
    elif 'upper_intermediate' in filename_lower or 'upper-intermediate' in filename_lower:
        return 'Upper_Intermediate'
    elif 'intermediate' in filename_lower:
        return 'Intermediate'
    elif 'advanced' in filename_lower:
        return 'Advanced'
    else:
        return 'Unknown'


def fix_unknown_files():
    """Move files from Unknown folder to correct level folders"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           FIX UNKNOWN FILES - MOVE TO CORRECT LEVELS                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    base_dir = Path("youtube_descriptions")
    unknown_folder = base_dir / "Unknown"
    
    if not unknown_folder.exists():
        print("✅ No Unknown folder found!")
        return
    
    level_folders = {
        'Elementary': base_dir / 'Elementary',
        'Intermediate': base_dir / 'Intermediate',
        'Upper_Intermediate': base_dir / 'Upper_Intermediate',
        'Advanced': base_dir / 'Advanced'
    }
    
    # Ensure all level folders exist
    for folder in level_folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    
    stats = {
        'Elementary': 0,
        'Intermediate': 0,
        'Upper_Intermediate': 0,
        'Advanced': 0,
        'Still_Unknown': 0
    }
    
    unknown_files = list(unknown_folder.glob("video_*.html"))
    print(f"📊 Found {len(unknown_files)} files in Unknown folder\n")
    
    for html_file in unknown_files:
        level = get_level_from_filename(html_file.name)
        
        if level == 'Unknown':
            stats['Still_Unknown'] += 1
            print(f"⚠️  Still unknown: {html_file.name}")
            continue
        
        target_folder = level_folders[level]
        target_file = target_folder / html_file.name
        
        if target_file.exists():
            print(f"⏭️  Already exists: {html_file.name}")
            html_file.unlink()  # Delete from Unknown
            continue
        
        try:
            shutil.move(str(html_file), str(target_file))
            stats[level] += 1
            
            if stats[level] <= 5:
                print(f"✅ {html_file.name} → {level}")
        except Exception as e:
            print(f"❌ Error moving {html_file.name}: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("📊 FIX SUMMARY")
    print("="*80)
    
    for level, count in stats.items():
        if count > 0:
            if level != 'Still_Unknown':
                folder = level_folders[level]
                total_in_folder = len(list(folder.glob("video_*.html")))
                print(f"   {level}: +{count} files (Total: {total_in_folder})")
            else:
                print(f"   Still Unknown: {count} files")
    
    # Check if Unknown folder is empty
    remaining = len(list(unknown_folder.glob("video_*.html")))
    
    if remaining == 0:
        print(f"\n✅ Unknown folder is now empty!")
        try:
            unknown_folder.rmdir()
            print(f"✅ Deleted empty Unknown folder")
        except:
            pass
    else:
        print(f"\n⚠️  {remaining} files still in Unknown folder")
    
    print("\n" + "="*80)
    print("📁 FINAL FOLDER STRUCTURE")
    print("="*80)
    
    grand_total = 0
    for level, folder in level_folders.items():
        if folder.exists():
            file_count = len(list(folder.glob("video_*.html")))
            if file_count > 0:
                print(f"   {level}: {file_count} episodes")
                grand_total += file_count
    
    print(f"\n🎉 TOTAL: {grand_total} episodes organized by level!")


if __name__ == '__main__':
    fix_unknown_files()
