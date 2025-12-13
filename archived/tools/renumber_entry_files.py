#!/usr/bin/env python3
"""
Renumber Entry_02 and Entry_03 audio files to match conversation files

Entry_02: 001-100 -> 101-200
Entry_03: 001-063 -> 201-263
"""

from pathlib import Path
import re

def renumber_files(folder: Path, offset: int):
    """Renumber files in folder by adding offset to episode number"""
    print(f"\n📁 Processing: {folder.name}")
    print(f"   Offset: +{offset}")
    
    files = sorted(folder.glob('*.m4a'))
    print(f"   Found {len(files)} files")
    
    renamed = 0
    for file in files:
        # Extract episode number from filename
        match = re.match(r'^(\d{3})_(.*)\.m4a$', file.name)
        if match:
            old_num = int(match.group(1))
            rest = match.group(2)
            new_num = old_num + offset
            
            new_name = f"{new_num:03d}_{rest}.m4a"
            new_path = folder / new_name
            
            if file.name != new_name:
                file.rename(new_path)
                print(f"   ✅ {file.name} → {new_name}")
                renamed += 1
        else:
            print(f"   ⚠️  Could not parse: {file.name}")
    
    print(f"   Renamed {renamed} files\n")

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           RENUMBER ENTRY_02 AND ENTRY_03 AUDIO FILES                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    base = Path('resources/audio')
    
    # Renumber Entry_02: 001-100 -> 101-200
    entry_02 = base / 'Entry_02'
    if entry_02.exists():
        renumber_files(entry_02, 100)
    
    # Renumber Entry_03: 001-063 -> 201-263
    entry_03 = base / 'Entry_03'
    if entry_03.exists():
        renumber_files(entry_03, 200)
    
    print("="*80)
    print("✅ Renumbering complete!")
    print("="*80)

if __name__ == '__main__':
    main()
