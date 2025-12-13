#!/usr/bin/env python3
"""
Quick test script to add pronunciations to just the first 10 episodes
"""

import json
import requests
import time
from pathlib import Path

DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

def clean_word(word_with_category):
    import re
    match = re.match(r'^(.+?)\s*\([^)]+\)$', word_with_category)
    if match:
        return match.group(1).strip()
    return word_with_category.strip()

def get_pronunciation(word):
    try:
        clean = clean_word(word)
        response = requests.get(DICTIONARY_API.format(word=clean.replace(' ', '%20')), timeout=5)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        for entry in data:
            if 'phonetics' in entry:
                for phonetic in entry['phonetics']:
                    if 'text' in phonetic and phonetic.get('text'):
                        return phonetic['text'].strip('/')
        return None
    except:
        return None

# Load JSON
json_path = Path('src/data/all-episodes-mapped.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Adding pronunciations to first 10 episodes...\n")

# Process only first 10 episodes
for episode_idx, episode in enumerate(data[:10]):
    print(f"Episode {episode.get('id')}: {episode.get('title')}")
    
    if 'transcript' in episode and 'vocabulary' in episode['transcript']:
        for vocab_item in episode['transcript']['vocabulary'][:5]:  # Only first 5 words per episode
            word = vocab_item.get('word', '')
            if 'pronunciation' not in vocab_item:
                print(f"  Fetching: {clean_word(word)}...", end=' ')
                pronunciation = get_pronunciation(word)
                if pronunciation:
                    vocab_item['pronunciation'] = pronunciation
                    print(f"✓ /{pronunciation}/")
                else:
                    print("✗")
                time.sleep(0.3)

# Save
backup_path = json_path.with_suffix('.json.backup-test')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ Done! Check the app to see IPA pronunciations.")
