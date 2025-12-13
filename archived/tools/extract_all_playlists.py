#!/usr/bin/env python3
"""
Master Extraction Script - Run All Playlists Sequentially

This script runs all playlist extractions in order:
1. Elementary
2. Intermediate  
3. Upper Intermediate
4. Advanced

Each extraction will auto-rename files after completion.
"""

import subprocess
import sys
from pathlib import Path


def run_extraction(script_name, playlist_name):
    """Run an extraction script and wait for completion"""
    print(f"\n{'='*80}")
    print(f"🚀 STARTING: {playlist_name}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path.cwd(),
            check=True
        )
        
        print(f"\n✅ COMPLETED: {playlist_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FAILED: {playlist_name}")
        print(f"Error: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️  INTERRUPTED: {playlist_name}")
        return False


def main():
    """Run all extractions sequentially"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     MASTER EXTRACTION SCRIPT                                 ║
║                     Extract All Playlists                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

This will extract all EnglishPod playlists in order:
  1. Elementary
  2. Intermediate
  3. Upper Intermediate
  4. Advanced

Each extraction includes automatic file renaming.
Press Ctrl+C to stop at any time.

    """)
    
    input("Press Enter to start...")
    
    extractions = [
        ("extract_elementary.py", "Elementary"),
        ("extract_intermediate.py", "Intermediate"),
        ("extract_upper_intermediate.py", "Upper Intermediate"),
        ("extract_advanced.py", "Advanced"),
    ]
    
    results = {}
    
    for script, name in extractions:
        success = run_extraction(script, name)
        results[name] = success
        
        if not success:
            print(f"\n⚠️  Stopping due to failure in {name}")
            break
    
    # Final summary
    print("\n" + "="*80)
    print("📊 FINAL SUMMARY")
    print("="*80)
    
    for name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {name}")
    
    print("\n" + "="*80)
    
    # Count folders
    base_dir = Path("youtube_descriptions")
    if base_dir.exists():
        folders = [
            "Elementary",
            "Intermediate", 
            "Upper_Intermediate",
            "Advanced"
        ]
        
        print("\n📁 EXTRACTED FILES:")
        total_files = 0
        
        for folder in folders:
            folder_path = base_dir / folder
            if folder_path.exists():
                files = list(folder_path.glob("*.html"))
                count = len(files)
                total_files += count
                print(f"  {folder}: {count} files")
        
        print(f"\n🎉 TOTAL: {total_files} episodes extracted!")
    
    print("\n" + "="*80)
    print("✅ All extractions complete!")
    print("="*80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Master extraction interrupted by user")
        sys.exit(1)
