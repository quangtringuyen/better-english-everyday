#!/usr/bin/env python3
"""
Process YouTube Descriptions - Batch Processor

This script processes all HTML files in the youtube_descriptions folder
and generates a complete TypeScript episodes file.

Usage:
    python process_descriptions.py
"""

import re
import json
from pathlib import Path
from extract_youtube_data import parse_description, generate_typescript_episode


def extract_video_id_from_filename(filename: str) -> str:
    """Extract video number from filename like 'video_1.html'"""
    match = re.search(r'video_(\d+)', filename)
    if match:
        return f"video_{match.group(1)}"
    return filename.replace('.html', '')


def process_all_descriptions():
    """Process all HTML files in youtube_descriptions/Episode_01 folder"""
    
    descriptions_dir = Path('youtube_descriptions/Episode_01')
    
    if not descriptions_dir.exists():
        print("❌ Error: youtube_descriptions/Episode_01 folder not found!")
        print("Run 'python extract_playlist.py' first to create it.")
        return
    
    # Find all HTML files
    html_files = sorted(descriptions_dir.glob('*.html'))
    
    if not html_files:
        print("❌ No HTML files found in youtube_descriptions/Episode_01 folder!")
        print("\nPlease add HTML files following the instructions in extract_playlist.py")
        return
    
    print(f"📁 Found {len(html_files)} HTML files to process\n")
    
    all_episodes = []
    errors = []
    
    for idx, html_file in enumerate(html_files, 1):
        print(f"Processing {html_file.name}...")
        
        try:
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse the description
            data = parse_description(html_content)
            
            # Use actual video ID if available, otherwise use filename
            video_id = extract_video_id_from_filename(html_file.name)
            
            # Generate TypeScript code
            ts_code = generate_typescript_episode(data, video_id, idx)
            
            all_episodes.append({
                'id': idx,
                'filename': html_file.name,
                'title': data['title'],
                'level': data['level'],
                'ts_code': ts_code,
                'data': data
            })
            
            print(f"  ✅ {data['title']}")
            print(f"     - {len(data['conversation'])} dialogue lines")
            print(f"     - {len(data['keyVocabulary'])} key vocabulary items")
            print(f"     - {len(data['supplementaryVocabulary'])} supplementary vocabulary items\n")
            
        except Exception as e:
            errors.append({
                'file': html_file.name,
                'error': str(e)
            })
            print(f"  ❌ Error: {e}\n")
    
    if not all_episodes:
        print("❌ No episodes were successfully processed!")
        return
    
    # Generate complete TypeScript file
    print("="*80)
    print(f"\n📝 Generating TypeScript file with {len(all_episodes)} episodes...\n")
    
    ts_episodes = ',\n\n'.join([ep['ts_code'] for ep in all_episodes])
    
    complete_ts_file = f'''import type {{ Episode }} from '../types';

/**
 * YouTube EnglishPod Episodes
 * Auto-generated from YouTube video descriptions
 * 
 * Total Episodes: {len(all_episodes)}
 * Generated: {Path.cwd()}
 */

export const youtubeEpisodes: Episode[] = [
{ts_episodes}
];

// Export for use in the application
export default youtubeEpisodes;
'''
    
    # Save to TypeScript file
    output_file = Path('src/data/youtube-episodes-generated.ts')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(complete_ts_file)
    
    print(f"✅ TypeScript file saved: {output_file}")
    
    # Save JSON data for reference
    json_output = Path('youtube_episodes_data.json')
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump([ep['data'] for ep in all_episodes], f, indent=2)
    
    print(f"✅ JSON data saved: {json_output}")
    
    # Print summary
    print("\n" + "="*80)
    print("📊 EXTRACTION SUMMARY")
    print("="*80)
    print(f"✅ Successfully processed: {len(all_episodes)} episodes")
    if errors:
        print(f"❌ Errors: {len(errors)} files")
        for err in errors:
            print(f"   - {err['file']}: {err['error']}")
    
    print("\n📚 Episodes extracted:")
    for ep in all_episodes:
        print(f"   {ep['id']}. {ep['title']} ({ep['level']})")
    
    print("\n" + "="*80)
    print("🎉 NEXT STEPS:")
    print("="*80)
    print(f"1. Review the generated file: {output_file}")
    print("2. Update src/App.tsx to import from youtube-episodes-generated.ts")
    print("3. Run 'npm run dev' to see your episodes in the app!")
    print("\n💡 The app will automatically display all episodes with:")
    print("   - Color-coded vocabulary badges")
    print("   - Categorized grammar types")
    print("   - Separate Key and Supplementary vocabulary sections")
    print("="*80 + "\n")


if __name__ == '__main__':
    process_all_descriptions()
