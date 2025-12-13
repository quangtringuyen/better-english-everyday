#!/usr/bin/env python3
"""
Map Audio Files to Conversations and Generate Unified Data Structure

This script:
1. Scans resources/audio and resources/conversation folders
2. Maps audio files to their corresponding conversation HTML files
3. Parses HTML to extract dialogue and vocabulary
4. Generates a unified JSON structure for the app
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

# Folder mappings (now they match!)
FOLDER_MAPPINGS = {
    'Entry_01': 'Entry_01',
    'Entry_02': 'Entry_02',
    'Entry_03': 'Entry_03',
    'Elementary': 'Elementary',
    'Intermediate': 'Intermediate',
    'Upper_Intermediate': 'Upper_Intermediate',
    'Advanced': 'Advanced'
}

def extract_episode_number(filename: str) -> Optional[int]:
    """Extract episode number from filename"""
    # Try to match patterns like "001", "01", "video_001", "EnglishPod_1"
    patterns = [
        r'^(\d{3})',  # 001 at start (3 digits)
        r'^(\d{1,2})\s*-',  # 01 - or 1 - at start (1-2 digits followed by dash)
        r'video_(\d{3})',  # video_001
        r'EnglishPod_(\d+)',  # EnglishPod_1
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
    
    return None


def parse_conversation_html(html_path: Path) -> Dict:
    """Parse conversation HTML and extract structured data"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_match = re.search(r'EnglishPod \d+ - (.*?) - (.*?)(?:\n|$)', soup.get_text())
    level = title_match.group(1).strip() if title_match else "Unknown"
    topic = title_match.group(2).strip() if title_match else "Unknown"
    
    # Extract conversation
    text = soup.get_text()
    dialogue = []
    
    # Find conversation section
    conv_start = text.find('Conversation')
    key_vocab_start = text.find('Key Vocabulary')
    
    if conv_start != -1 and key_vocab_start != -1:
        conv_text = text[conv_start:key_vocab_start]
        lines = conv_text.split('\n')
        
        for line in lines[1:]:  # Skip "Conversation" header
            line = line.strip()
            if not line:
                continue
            
            # Match dialogue lines like "A:  Text" or "B:  Text"
            match = re.match(r'^([AB]):\s+(.+)$', line)
            if match:
                speaker = match.group(1)
                text = match.group(2).replace('\u00a0', ' ').strip()
                dialogue.append({
                    'speaker': speaker,
                    'text': text
                })
    
    # Extract vocabulary
    vocabulary = []
    supplementary_vocabulary = []
    
    # Find all list items
    for li in soup.find_all('li'):
        vocab_text = li.get_text().strip()
        if ':' in vocab_text:
            parts = vocab_text.split(':', 1)
            word = parts[0].strip()
            definition = parts[1].strip() if len(parts) > 1 else ""
            
            vocab_item = {
                'word': word,
                'definition': definition
            }
            
            # Determine if it's key or supplementary based on position
            if 'Supplementary' in text[:text.find(vocab_text)] if vocab_text in text else False:
                supplementary_vocabulary.append(vocab_item)
            else:
                vocabulary.append(vocab_item)
    
    return {
        'level': level,
        'topic': topic,
        'dialogue': dialogue,
        'vocabulary': vocabulary,
        'supplementaryVocabulary': supplementary_vocabulary
    }


def map_audio_to_conversations() -> List[Dict]:
    """Map audio files to their conversations and create unified structure"""
    episodes = []
    
    audio_base = Path('resources/audio')
    conv_base = Path('resources/conversation')
    
    for audio_folder, conv_folder in FOLDER_MAPPINGS.items():
        audio_dir = audio_base / audio_folder
        conv_dir = conv_base / conv_folder
        
        if not audio_dir.exists() or not conv_dir.exists():
            print(f"⚠️  Skipping {audio_folder}: folder not found")
            continue
        
        print(f"\n📁 Processing {audio_folder} -> {conv_folder}")
        
        # Get all audio files
        audio_files = sorted(audio_dir.glob('*.m4a'))
        
        for audio_file in audio_files:
            # Try new filename format first: 001_Elementary_Difficult_Customer.m4a
            match = re.match(r'^(\d{3})_(.*)\.m4a$', audio_file.name)
            
            if match:
                # New format
                episode_num = int(match.group(1))
                rest = match.group(2)  # Level_Topic
                
                # Split level and topic
                parts = rest.split('_', 1)
                if len(parts) >= 2:
                    level = parts[0].replace('_', ' ')
                    topic = parts[1].replace('_', ' ')
                else:
                    level = "Unknown"
                    topic = rest.replace('_', ' ')
            else:
                # Try old format: 01 - Topic.m4a or 001 - Topic.m4a
                match_old = re.match(r'^(\d{1,3})\s*-\s*(.*)\.m4a$', audio_file.name)
                if not match_old:
                    print(f"  ⚠️  Could not parse audio file: {audio_file.name}")
                    continue
                
                episode_num = int(match_old.group(1))
                topic = match_old.group(2).strip()
                level = "Unknown"  # Will try to get from conversation file
            
            # Find matching conversation file
            conv_file = None
            
            # Try exact match first (same base name)
            conv_file_name = audio_file.stem + '.html'
            conv_file_path = conv_dir / conv_file_name
            
            if conv_file_path.exists():
                conv_file = conv_file_path
            else:
                # Try to find by episode number (for old format files)
                conv_files = list(conv_dir.glob(f'{episode_num:03d}_*.html'))
                if conv_files:
                    conv_file = conv_files[0]
                    # Extract level from conversation filename if we don't have it
                    if level == "Unknown":
                        conv_match = re.match(r'^\d{3}_([^_]+)_', conv_file.name)
                        if conv_match:
                            level = conv_match.group(1)
            
            # Parse conversation if it exists, otherwise create empty transcript
            conv_data = {
                'dialogue': [],
                'vocabulary': [],
                'supplementaryVocabulary': []
            }
            
            if conv_file and conv_file.exists():
                try:
                    conv_data = parse_conversation_html(conv_file)
                except Exception as e:
                    print(f"  ⚠️  Error parsing conversation for episode {episode_num}: {e}")
            else:
                print(f"  ℹ️  No conversation for episode {episode_num} (audio only)")
            
            episode = {
                'id': episode_num,
                'title': f"{level} - {topic}",
                'level': level,
                'folder': conv_folder,
                'description': f"Learn {topic.lower()} through this lesson.",
                'audioUrl': f"/resources/audio/{audio_folder}/{audio_file.name}",
                'transcript': {
                    'dialogue': conv_data['dialogue'],
                    'vocabulary': conv_data['vocabulary'],
                    'supplementaryVocabulary': conv_data['supplementaryVocabulary']
                }
            }
            
            episodes.append(episode)
            print(f"  ✅ Episode {episode_num}: {topic}")
    
    return episodes


def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AUDIO-CONVERSATION MAPPER                                          ║
║           Generate Unified Data Structure                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Map audio to conversations
    episodes = map_audio_to_conversations()
    
    # Sort by folder and episode number within folder
    episodes.sort(key=lambda x: (x['folder'], x['id']))
    
    # Assign globally unique IDs
    for idx, episode in enumerate(episodes, 1):
        episode['originalId'] = episode['id']  # Keep original for reference
        episode['id'] = idx  # Assign new unique ID
    
    # Save to JSON
    output_file = Path('src/data/all-episodes-mapped.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(episodes, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"📊 MAPPING SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Total episodes mapped: {len(episodes)}")
    print(f"📁 Output file: {output_file.absolute()}")
    
    # Count by folder
    folder_counts = {}
    for ep in episodes:
        folder = ep['folder']
        folder_counts[folder] = folder_counts.get(folder, 0) + 1
    
    print(f"\n📂 Episodes by folder:")
    for folder, count in sorted(folder_counts.items()):
        print(f"  {folder}: {count} episodes")
    
    print(f"\n{'='*80}")
    print(f"✅ Mapping complete!")
    print(f"✅ All episodes have unique IDs (1-{len(episodes)})")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
