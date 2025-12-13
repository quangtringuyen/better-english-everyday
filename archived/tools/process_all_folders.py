#!/usr/bin/env python3
"""
Process ALL YouTube Descriptions from 7 Folders

This script processes HTML files from all 7 folders in the correct order:
1. Entry_01
2. Entry_02
3. Entry_03
4. Elementary
5. Intermediate
6. Upper_Intermediate
7. Advanced

Generates: src/data/all-episodes-generated.ts
"""

import re
import json
from pathlib import Path
from extract_youtube_data import parse_description, generate_typescript_episode


def extract_video_id_from_filename(filename: str) -> str:
    """Extract video number from filename"""
    match = re.search(r'video_(\d+)', filename)
    if match:
        return f"video_{match.group(1)}"
    return filename.replace('.html', '')


def process_folder(folder_name: str, start_id: int):
    """Process all HTML files in a specific folder"""
    
    folder_path = Path(f'youtube_descriptions/{folder_name}')
    
    if not folder_path.exists():
        print(f"⚠️  {folder_name} folder not found, skipping...")
        return [], start_id
    
    html_files = sorted(folder_path.glob('*.html'))
    
    if not html_files:
        print(f"⚠️  No HTML files in {folder_name}, skipping...")
        return [], start_id
    
    print(f"\n📁 Processing {folder_name}...")
    print(f"   Found {len(html_files)} files")
    
    episodes = []
    current_id = start_id
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            episode_data = parse_description(html_content)
            
            if episode_data:
                episode_data['id'] = current_id
                episode_data['folder'] = folder_name
                
                # Fallback: validation of title
                if not episode_data['title']:
                    # Try to extract from filename
                    # Filename: video_083_EnglishPod_83_-_... .html
                    clean_name = html_file.stem  # video_083_EnglishPod...
                    # Remove video_XXX_ prefix
                    if re.match(r'video_\d+_', clean_name):
                        clean_name = re.sub(r'video_\d+_', '', clean_name)
                    
                    # Replace underscores with spaces
                    clean_name = clean_name.replace('_', ' ')
                    
                    # If it looks like a valid title, use it
                    if len(clean_name) > 5:
                        print(f"   ⚠️  Recovered title from filename: {clean_name}")
                        episode_data['title'] = clean_name
                        
                        # Try to extract level from filename if missing
                        if not episode_data['level']:
                            if 'Elementary' in clean_name:
                                episode_data['level'] = 'Elementary'
                            elif 'Intermediate' in clean_name:  # Covers Upper Intermediate too if we check simplistic
                                if 'Upper Intermediate' in clean_name:
                                    episode_data['level'] = 'Upper Intermediate'
                                else:
                                    episode_data['level'] = 'Intermediate'
                            elif 'Advanced' in clean_name:
                                episode_data['level'] = 'Advanced'

                episodes.append(episode_data)
                current_id += 1
        except Exception as e:
            print(f"   ❌ Error processing {html_file.name}: {e}")
    
    print(f"   ✅ Processed {len(episodes)} episodes")
    return episodes, current_id


def process_all_folders():
    """Process all 7 folders in the correct order"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           PROCESS ALL EPISODES - 7 FOLDERS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Folders in the correct order
    folders = [
        'Entry_01',
        'Entry_02',
        'Entry_03',
        'Elementary',
        'Intermediate',
        'Upper_Intermediate',
        'Advanced'
    ]
    
    all_episodes = []
    current_id = 1
    
    # Process each folder
    for folder in folders:
        episodes, current_id = process_folder(folder, current_id)
        all_episodes.extend(episodes)
    
    if not all_episodes:
        print("\n❌ No episodes were processed!")
        return
    
    print("\n" + "="*80)
    print("📊 PROCESSING SUMMARY")
    print("="*80)
    print(f"✅ Total episodes processed: {len(all_episodes)}")
    
    # Generate TypeScript file
    output_file = Path('src/data/all-episodes-generated.ts')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📝 Generating TypeScript file...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("import type { Episode } from '../types';\n\n")
        f.write("// Auto-generated from YouTube descriptions\n")
        f.write(f"// Total episodes: {len(all_episodes)}\n")
        f.write("// Generated from 7 folders in order:\n")
        f.write("// 1. Entry_01, 2. Entry_02, 3. Entry_03\n")
        f.write("// 4. Elementary, 5. Intermediate, 6. Upper_Intermediate, 7. Advanced\n\n")
        f.write("const allEpisodes: Episode[] = [\n")
        
        for idx, episode in enumerate(all_episodes):
            video_id = f"ep{episode['id']}"
            episode_num = episode['id']
            folder = episode.get('folder', 'Unknown')
            
            # Generate TypeScript with folder field
            ts_code = generate_typescript_episode(episode, video_id, episode_num)
            
            # Insert folder field after level field
            # Find the level line and add folder after it
            lines = ts_code.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if 'level:' in line:
                    # Add folder field right after level
                    indent = '    '
                    new_lines.append(f'{indent}folder: "{folder}",')
            
            ts_code = '\n'.join(new_lines)
            f.write(ts_code)
            if idx < len(all_episodes) - 1:
                f.write(',\n')
        
        
        f.write("\n];\n\n")
        f.write("export default allEpisodes;\n")
    
    print(f"✅ Generated: {output_file}")
    
    # Also save JSON backup
    json_file = Path('all_episodes_data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_episodes, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON backup: {json_file}")
    
    # Summary by folder
    print("\n" + "="*80)
    print("📁 EPISODES BY FOLDER")
    print("="*80)
    
    folder_counts = {}
    for episode in all_episodes:
        folder = episode.get('folder', 'Unknown')
        folder_counts[folder] = folder_counts.get(folder, 0) + 1
    
    for folder in folders:
        count = folder_counts.get(folder, 0)
        if count > 0:
            print(f"   {folder}: {count} episodes")
    
    print("\n" + "="*80)
    print("✅ COMPLETE!")
    print("="*80)
    print(f"""
All {len(all_episodes)} episodes have been processed and saved to:
  {output_file}

Next steps:
1. Update src/App.tsx to import from './data/all-episodes-generated'
2. Run 'npm run dev' to test
3. Check the app in your browser

🎉 You now have {len(all_episodes)} EnglishPod episodes in your app!
    """)


if __name__ == '__main__':
    process_all_folders()
