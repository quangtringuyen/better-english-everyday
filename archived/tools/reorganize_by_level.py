#!/usr/bin/env python3
"""
Reorganize ALL episodes by difficulty level

This script will:
1. Find all HTML files in audio_source/Entry_* folders
2. Parse each file to determine the difficulty level
3. Copy files to appropriate level folders in youtube_descriptions/
"""

import re
from pathlib import Path
from html import unescape
import shutil


def parse_level_from_html(html_file):
    """Extract the difficulty level from HTML content"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove HTML tags but keep structure
        text = unescape(content)
        text = re.sub(r'<[^>]+>', '\n', text)
        
        # Look for level indicators
        if 'Elementary' in text:
            return 'Elementary'
        elif 'Upper Intermediate' in text or 'Upper-Intermediate' in text:
            return 'Upper_Intermediate'
        elif 'Intermediate' in text:
            return 'Intermediate'
        elif 'Advanced' in text:
            return 'Advanced'
        else:
            return 'Unknown'
    except Exception as e:
        print(f"Error parsing {html_file}: {e}")
        return 'Unknown'


def reorganize_all_by_level():
    """Reorganize all episode files by difficulty level"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           REORGANIZE ALL EPISODES BY DIFFICULTY LEVEL                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Source folders
    source_base = Path("audio_source")
    source_folders = ['Entry_01', 'Entry_02', 'Entry_03']
    
    # Target folders (level-based)
    target_base = Path("youtube_descriptions")
    level_folders = {
        'Elementary': target_base / 'Elementary',
        'Intermediate': target_base / 'Intermediate',
        'Upper_Intermediate': target_base / 'Upper_Intermediate',
        'Advanced': target_base / 'Advanced',
        'Unknown': target_base / 'Unknown'
    }
    
    # Ensure all level folders exist
    for folder in level_folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    
    stats = {
        'Elementary': 0,
        'Intermediate': 0,
        'Upper_Intermediate': 0,
        'Advanced': 0,
        'Unknown': 0
    }
    
    total_files = 0
    skipped = 0
    
    # Process each source folder
    for source_folder_name in source_folders:
        source_folder = source_base / source_folder_name
        
        if not source_folder.exists():
            print(f"⚠️  {source_folder_name} not found, skipping...")
            continue
        
        print(f"\n📁 Processing audio_source/{source_folder_name}...")
        
        html_files = list(source_folder.glob("video_*.html"))
        print(f"   Found {len(html_files)} files")
        
        for html_file in html_files:
            level = parse_level_from_html(html_file)
            
            # Check if file already exists in target folder
            target_folder = level_folders[level]
            target_file = target_folder / html_file.name
            
            if target_file.exists():
                skipped += 1
                continue
            
            # Copy file to level folder
            try:
                shutil.copy2(html_file, target_file)
                stats[level] += 1
                total_files += 1
                
                # Show first few files
                if stats[level] <= 3:
                    print(f"   ✅ {html_file.name} → {level}")
            except Exception as e:
                print(f"   ❌ Error copying {html_file.name}: {e}")
        
        if stats['Elementary'] + stats['Intermediate'] + stats['Upper_Intermediate'] + stats['Advanced'] > 3:
            print(f"   ... and more files")
    
    # Summary
    print("\n" + "="*80)
    print("📊 REORGANIZATION SUMMARY")
    print("="*80)
    
    for level, count in stats.items():
        if count > 0:
            folder = level_folders[level]
            total_in_folder = len(list(folder.glob("video_*.html")))
            print(f"   {level}: +{count} new files (Total: {total_in_folder})")
    
    print(f"\n📈 Total files copied: {total_files}")
    print(f"⏭️  Files skipped (already exist): {skipped}")
    
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
    
    print(f"\n🎉 GRAND TOTAL: {grand_total} episodes organized by level!")
    
    print("\n" + "="*80)
    print("✅ COMPLETE!")
    print("="*80)
    print("""
All episodes from audio_source/Entry_* have been organized by difficulty level!

Folder structure:
  youtube_descriptions/
  ├── Elementary/          (All elementary episodes)
  ├── Intermediate/        (All intermediate episodes)
  ├── Upper_Intermediate/  (All upper intermediate episodes)
  └── Advanced/            (All advanced episodes)

Original files in audio_source/Entry_* are kept intact.
    """)


if __name__ == '__main__':
    reorganize_all_by_level()
