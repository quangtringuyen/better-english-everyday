#!/usr/bin/env python3
"""
Script to reorder and renumber episodes by difficulty level.
Order: Elementary > Entry_01 > Entry_02 > Entry_03 > Advanced
"""

import json
from pathlib import Path

def get_level_order(episode):
    """Return sort order for difficulty levels based on folder."""
    folder = episode.get('folder', '')
    level = episode.get('level', '')
    
    # Map folders to order
    folder_map = {
        'Elementary': 0,
        'Entry_01': 1,
        'Entry_02': 2,
        'Entry_03': 3,
        'Advanced': 4
    }
    
    # Try folder first, then level
    if folder in folder_map:
        return folder_map[folder]
    elif level in folder_map:
        return folder_map[level]
    else:
        return 999  # Unknown goes last

def reorder_episodes(json_path, dry_run=True):
    """
    Reorder episodes by difficulty level and renumber them sequentially.
    
    Args:
        json_path: Path to all-episodes-mapped.json
        dry_run: If True, don't save changes (default: True)
    """
    print(f"\n{'='*60}")
    print(f"Reordering episodes in: {json_path}")
    print(f"Mode: {'DRY RUN (no changes will be saved)' if dry_run else 'LIVE (will update file)'}")
    print(f"{'='*60}\n")
    
    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        episodes = json.load(f)
    
    print(f"📊 Total episodes: {len(episodes)}\n")
    
    # Show current order (first 10)
    print("Current order (first 10):")
    for i, ep in enumerate(episodes[:10], 1):
        folder = ep.get('folder', 'Unknown')
        print(f"  {i}. [{folder:12}] {ep.get('title', 'Unknown')}")
    print()
    
    # Sort episodes by level, then by original ID
    sorted_episodes = sorted(episodes, key=lambda ep: (
        get_level_order(ep),
        ep.get('id', 0)
    ))
    
    # Renumber episodes
    for new_id, episode in enumerate(sorted_episodes, start=1):
        old_id = episode['id']
        episode['id'] = new_id
        folder = episode.get('folder', 'Unknown')
        if new_id <= 10 or old_id != new_id:
            print(f"  Episode {old_id:3d} → {new_id:3d}: [{folder:12}] {episode.get('title', 'Unknown')}")
    
    # Show new order (first 10)
    print(f"\nNew order (first 10):")
    for i, ep in enumerate(sorted_episodes[:10], 1):
        folder = ep.get('folder', 'Unknown')
        print(f"  {i}. [{folder:12}] {ep.get('title', 'Unknown')}")
    
    # Show last 10
    print(f"\nNew order (last 10):")
    for i, ep in enumerate(sorted_episodes[-10:], len(sorted_episodes) - 9):
        folder = ep.get('folder', 'Unknown')
        print(f"  {i}. [{folder:12}] {ep.get('title', 'Unknown')}")
    
    # Count by folder
    print(f"\n{'='*60}")
    print("Episodes by folder:")
    print(f"{'='*60}")
    folder_counts = {}
    for ep in sorted_episodes:
        folder = ep.get('folder', 'Unknown')
        folder_counts[folder] = folder_counts.get(folder, 0) + 1
    
    for folder in ['Elementary', 'Entry_01', 'Entry_02', 'Entry_03', 'Advanced', 'Unknown']:
        count = folder_counts.get(folder, 0)
        if count > 0:
            print(f"  {folder:12}: {count:3d} episodes")
    print(f"{'='*60}\n")
    
    # Save if not dry run
    if not dry_run:
        backup_path = json_path.with_suffix('.json.backup-reorder')
        print(f"💾 Creating backup: {backup_path}")
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(episodes, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saving reordered JSON: {json_path}")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_episodes, f, ensure_ascii=False, indent=2)
        
        print("✅ File updated successfully!")
    else:
        print("ℹ️  DRY RUN - No changes saved. Run with --live to save changes.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Reorder episodes by difficulty level')
    parser.add_argument('--live', action='store_true', help='Actually save changes (default is dry-run)')
    parser.add_argument('--file', type=str, default='src/data/all-episodes-mapped.json', 
                       help='Path to JSON file (default: src/data/all-episodes-mapped.json)')
    
    args = parser.parse_args()
    
    json_path = Path(args.file)
    
    if not json_path.exists():
        print(f"❌ Error: File not found: {json_path}")
        return
    
    reorder_episodes(json_path, dry_run=not args.live)

if __name__ == '__main__':
    main()
