#!/usr/bin/env python3
"""
Fix Entry_02 numbering mess

Current state:
- 087-100: Old format "087 - Topic.m4a"
- 201-286: Should be 101-186

Target:
- 101-200: Properly numbered and formatted
"""

from pathlib import Path
import re
import shutil

def fix_entry_02():
    folder = Path('resources/audio/Entry_02')
    
    print("Step 1: Renumber 201-286 back to 101-186")
    files = sorted(folder.glob('[2][0-9][0-9]_*.m4a'))
    for file in files:
        match = re.match(r'^(\d{3})_(.*)\.m4a$', file.name)
        if match:
            old_num = int(match.group(1))
            rest = match.group(2)
            new_num = old_num - 100  # 201 -> 101, 286 -> 186
            new_name = f"{new_num:03d}_{rest}.m4a"
            new_path = folder / new_name
            file.rename(new_path)
            print(f"  {file.name} -> {new_name}")
    
    print("\nStep 2: Rename and renumber 087-100 to 187-200")
    old_format_files = sorted(folder.glob('[0-9][0-9][0-9] - *.m4a'))
    for file in old_format_files:
        # Extract number and topic from "087 - Going On A Diet.m4a"
        match = re.match(r'^(\d{3}) - (.*)\.m4a$', file.name)
        if match:
            old_num = int(match.group(1))
            topic = match.group(2)
            
            # Determine level (we'll use Elementary as default, can be adjusted)
            # For now, let's extract from conversation files
            new_num = old_num + 100  # 087 -> 187, 100 -> 200
            
            # Sanitize topic
            safe_topic = topic.replace(' ', '_').replace("'", '')
            
            # We need to determine the level - let's check conversation file
            conv_file = Path(f'resources/conversation/Entry_02/{new_num:03d}_*.html')
            conv_files = list(Path('resources/conversation/Entry_02').glob(f'{new_num:03d}_*.html'))
            
            if conv_files:
                # Extract level from conversation filename
                conv_match = re.match(r'^\d{3}_([^_]+)_', conv_files[0].name)
                level = conv_match.group(1) if conv_match else 'Elementary'
            else:
                level = 'Elementary'  # Default
            
            new_name = f"{new_num:03d}_{level}_{safe_topic}.m4a"
            new_path = folder / new_name
            file.rename(new_path)
            print(f"  {file.name} -> {new_name}")
    
    print("\n✅ Entry_02 fixed!")

if __name__ == '__main__':
    fix_entry_02()
