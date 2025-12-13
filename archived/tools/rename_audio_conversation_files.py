#!/usr/bin/env python3
"""
Rename Audio and Conversation Files with Consistent Naming

This script renames both audio and conversation files to have a consistent
naming pattern that makes their linkage clear:

Format: {episode_number:03d}_{level}_{topic}.{ext}
Example: 001_Elementary_Difficult_Customer.m4a
         001_Elementary_Difficult_Customer.html
"""

import re
from pathlib import Path
from typing import Dict, Optional, Tuple

# Folder mappings
FOLDER_MAPPINGS = {
    'Entry_Level_01': 'Entry_01',
    'Entry_Level_02': 'Entry_02',
    'Entry_Level_03': 'Entry_03',
    'Elementary': 'Elementary',
    'Intermediate': 'Intermediate',
    'Upper_Intermediate': 'Upper_Intermediate',
    'Advance': 'Advanced'
}


def sanitize_filename(text: str) -> str:
    """Convert text to safe filename component"""
    # Remove special characters and replace spaces with underscores
    safe = re.sub(r'[^\w\s-]', '', text)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    safe = re.sub(r"'", '', safe)  # Remove apostrophes
    return safe.strip('_')


def extract_episode_info(filename: str, is_audio: bool = True) -> Optional[Tuple[int, str, str]]:
    """Extract episode number, level, and topic from filename"""
    
    if is_audio:
        # Audio patterns: "001 - Elementary - Difficult Customer.m4a"
        # or "01 - Elementary - Topic.m4a"
        patterns = [
            r'^(\d{3})\s*-\s*(.*?)\s*-\s*(.*?)\.m4a$',  # 001 - Level - Topic
            r'^(\d{1,2})\s*-\s*(.*?)\s*-\s*(.*?)\.m4a$',  # 01 - Level - Topic
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                num = int(match.group(1))
                level = match.group(2).strip()
                topic = match.group(3).strip()
                return (num, level, topic)
    else:
        # Conversation patterns: "video_001_EnglishPod_1_-_Elementary_-_Difficult_Customer.html"
        patterns = [
            r'video_(\d{3})_EnglishPod_\d+_-_(.*?)_-_(.*?)\.html$',
            r'video_(\d{3})_(.*?)\.html$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                num = int(match.group(1))
                if len(match.groups()) >= 3:
                    level = match.group(2).strip()
                    topic = match.group(3).strip()
                else:
                    # Parse from the full filename
                    parts = match.group(2).split('_-_')
                    if len(parts) >= 2:
                        level = parts[0].replace('EnglishPod_', '').strip()
                        topic = parts[1].strip()
                    else:
                        level = "Unknown"
                        topic = match.group(2).strip()
                return (num, level, topic)
    
    return None


def rename_files_in_folder(audio_dir: Path, conv_dir: Path, dry_run: bool = True):
    """Rename files in both audio and conversation folders"""
    
    print(f"\n{'='*80}")
    print(f"📁 Processing: {audio_dir.name} <-> {conv_dir.name}")
    print(f"{'='*80}\n")
    
    if not audio_dir.exists():
        print(f"⚠️  Audio folder not found: {audio_dir}")
        return
    
    if not conv_dir.exists():
        print(f"⚠️  Conversation folder not found: {conv_dir}")
        return
    
    # Get all audio files
    audio_files = sorted(audio_dir.glob('*.m4a'))
    conv_files = sorted(conv_dir.glob('*.html'))
    
    print(f"📊 Found {len(audio_files)} audio files and {len(conv_files)} conversation files\n")
    
    renamed_count = 0
    
    # Process audio files
    for audio_file in audio_files:
        info = extract_episode_info(audio_file.name, is_audio=True)
        if not info:
            print(f"⚠️  Could not parse audio file: {audio_file.name}")
            continue
        
        num, level, topic = info
        safe_level = sanitize_filename(level)
        safe_topic = sanitize_filename(topic)
        
        new_name = f"{num:03d}_{safe_level}_{safe_topic}.m4a"
        new_path = audio_dir / new_name
        
        if audio_file.name != new_name:
            if dry_run:
                print(f"🔄 [DRY RUN] Audio: {audio_file.name}")
                print(f"           → {new_name}\n")
            else:
                try:
                    audio_file.rename(new_path)
                    print(f"✅ Renamed audio: {audio_file.name} → {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Error renaming {audio_file.name}: {e}")
    
    # Process conversation files
    for conv_file in conv_files:
        info = extract_episode_info(conv_file.name, is_audio=False)
        if not info:
            print(f"⚠️  Could not parse conversation file: {conv_file.name}")
            continue
        
        num, level, topic = info
        safe_level = sanitize_filename(level)
        safe_topic = sanitize_filename(topic)
        
        new_name = f"{num:03d}_{safe_level}_{safe_topic}.html"
        new_path = conv_dir / new_name
        
        if conv_file.name != new_name:
            if dry_run:
                print(f"🔄 [DRY RUN] Conv: {conv_file.name}")
                print(f"           → {new_name}\n")
            else:
                try:
                    conv_file.rename(new_path)
                    print(f"✅ Renamed conv: {conv_file.name} → {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Error renaming {conv_file.name}: {e}")
    
    if not dry_run:
        print(f"\n✅ Renamed {renamed_count} files in {audio_dir.name}")


def main():
    """Main function"""
    import sys
    
    # Check if --execute flag is provided
    dry_run = '--execute' not in sys.argv
    
    if dry_run:
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AUDIO & CONVERSATION FILE RENAMER (DRY RUN)                        ║
║           This will show what would be renamed without making changes        ║
║           Run with --execute to actually rename files                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
    else:
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AUDIO & CONVERSATION FILE RENAMER (EXECUTE MODE)                   ║
║           ⚠️  This will actually rename files!                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        response = input("Are you sure you want to proceed? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Aborted by user")
            return
    
    audio_base = Path('resources/audio')
    conv_base = Path('resources/conversation')
    
    # Process each folder pair
    for audio_folder, conv_folder in FOLDER_MAPPINGS.items():
        audio_dir = audio_base / audio_folder
        conv_dir = conv_base / conv_folder
        
        rename_files_in_folder(audio_dir, conv_dir, dry_run=dry_run)
    
    print(f"\n{'='*80}")
    if dry_run:
        print("✅ DRY RUN COMPLETE!")
        print("Run with --execute to actually rename files:")
        print("  python3 rename_audio_conversation_files.py --execute")
    else:
        print("✅ RENAMING COMPLETE!")
        print("All files have been renamed with consistent naming pattern:")
        print("  Format: {episode_number:03d}_{level}_{topic}.{ext}")
        print("  Example: 001_Elementary_Difficult_Customer.m4a")
        print("           001_Elementary_Difficult_Customer.html")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
