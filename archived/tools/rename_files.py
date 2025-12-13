#!/usr/bin/env python3
"""
Rename HTML files to include video titles

This script reads the HTML files, extracts the video title,
and renames the file to include the title.

Before: video_1.html
After:  video_001_EnglishPod_1_Elementary_Difficult_Customer.html

Usage:
    python3 rename_files.py
"""

import re
from pathlib import Path
from extract_youtube_data import parse_description


def sanitize_filename(title):
    """Convert title to safe filename"""
    # Remove special characters, keep alphanumeric, spaces, and hyphens
    safe = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe)
    # Remove multiple underscores
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


def rename_files():
    """Rename all HTML files in youtube_descriptions folder"""
    
    descriptions_dir = Path('youtube_descriptions')
    
    if not descriptions_dir.exists():
        print("❌ youtube_descriptions folder not found!")
        return
    
    # Find all HTML files
    html_files = sorted(descriptions_dir.glob('video_*.html'))
    
    if not html_files:
        print("❌ No HTML files found!")
        return
    
    print(f"📁 Found {len(html_files)} files to rename\n")
    
    renamed = 0
    skipped = 0
    
    for html_file in html_files:
        try:
            # Extract video number from current filename
            match = re.search(r'video_(\d+)', html_file.name)
            if not match:
                print(f"⚠️  Skipping {html_file.name} - can't extract number")
                skipped += 1
                continue
            
            video_num = int(match.group(1))
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse to get title
            data = parse_description(html_content)
            title = data.get('title', 'Unknown')
            
            if title == 'Unknown' or not title:
                print(f"⚠️  Skipping {html_file.name} - no title found")
                skipped += 1
                continue
            
            # Create new filename
            safe_title = sanitize_filename(title)
            new_filename = f"video_{video_num:03d}_{safe_title}.html"
            new_path = descriptions_dir / new_filename
            
            # Check if already renamed
            if html_file.name == new_filename:
                print(f"✓ Already renamed: {html_file.name}")
                skipped += 1
                continue
            
            # Rename the file
            html_file.rename(new_path)
            print(f"✅ Renamed: {html_file.name}")
            print(f"   → {new_filename}")
            renamed += 1
            
        except Exception as e:
            print(f"❌ Error renaming {html_file.name}: {e}")
            skipped += 1
    
    # Summary
    print("\n" + "="*80)
    print("📊 RENAME SUMMARY")
    print("="*80)
    print(f"✅ Renamed: {renamed} files")
    print(f"⚠️  Skipped: {skipped} files")
    print(f"📁 Location: {descriptions_dir.absolute()}")
    print("="*80)


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FILE RENAMER - Add Video Titles                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    rename_files()
    
    print("\n✅ Done! Files now include video titles in their names.")
