#!/usr/bin/env python3
"""
Script to add US IPA pronunciations to vocabulary items in all-episodes-mapped.json
Uses the Free Dictionary API to fetch pronunciation data.
"""

import json
import requests
import time
import re
from pathlib import Path

# API endpoint for dictionary lookups
DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

def clean_word(word_with_category):
    """
    Extract the clean word from entries like 'Dare to say (phrase)'
    Returns just the word/phrase without category info.
    """
    # Remove category in parentheses
    match = re.match(r'^(.+?)\s*\([^)]+\)$', word_with_category)
    if match:
        return match.group(1).strip()
    return word_with_category.strip()

def get_pronunciation(word):
    """
    Fetch US IPA pronunciation from Free Dictionary API.
    Returns the IPA string or None if not found.
    """
    try:
        # Clean the word first
        clean = clean_word(word)
        
        # Make API request
        response = requests.get(DICTIONARY_API.format(word=clean.replace(' ', '%20')), timeout=5)
        
        if response.status_code != 200:
            print(f"  ⚠️  No pronunciation found for '{clean}'")
            return None
        
        data = response.json()
        
        # Look for US pronunciation
        for entry in data:
            if 'phonetics' in entry:
                for phonetic in entry['phonetics']:
                    # Prefer US pronunciation
                    if 'text' in phonetic and phonetic.get('text'):
                        text = phonetic['text']
                        # Remove forward slashes if present
                        text = text.strip('/')
                        
                        # Check if it's US pronunciation (some APIs mark it)
                        if 'audio' in phonetic and 'us' in phonetic.get('audio', '').lower():
                            print(f"  ✓ Found US pronunciation: /{text}/")
                            return text
                
                # If no US-specific found, use the first available
                for phonetic in entry['phonetics']:
                    if 'text' in phonetic and phonetic.get('text'):
                        text = phonetic['text'].strip('/')
                        print(f"  ✓ Found pronunciation: /{text}/")
                        return text
        
        print(f"  ⚠️  No pronunciation in response for '{clean}'")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error fetching pronunciation for '{clean}': {e}")
        return None
    except Exception as e:
        print(f"  ❌ Unexpected error for '{clean}': {e}")
        return None

def add_pronunciations_to_json(json_path, dry_run=True, delay=0.5):
    """
    Add pronunciations to all vocabulary items in the JSON file.
    
    Args:
        json_path: Path to all-episodes-mapped.json
        dry_run: If True, don't save changes (default: True)
        delay: Delay between API calls in seconds (default: 0.5)
    """
    print(f"\n{'='*60}")
    print(f"Adding pronunciations to: {json_path}")
    print(f"Mode: {'DRY RUN (no changes will be saved)' if dry_run else 'LIVE (will update file)'}")
    print(f"{'='*60}\n")
    
    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_words = 0
    words_with_pronunciation = 0
    words_added = 0
    words_failed = 0
    
    # Process each episode
    for episode_idx, episode in enumerate(data):
        print(f"\n📚 Episode {episode.get('id', episode_idx)}: {episode.get('title', 'Unknown')}")
        
        # Process vocabulary
        if 'transcript' in episode and 'vocabulary' in episode['transcript']:
            for vocab_item in episode['transcript']['vocabulary']:
                total_words += 1
                word = vocab_item.get('word', '')
                
                # Skip if already has pronunciation
                if 'pronunciation' in vocab_item and vocab_item['pronunciation']:
                    words_with_pronunciation += 1
                    print(f"  ⏭️  '{clean_word(word)}' already has pronunciation")
                    continue
                
                # Fetch pronunciation
                print(f"  🔍 Fetching pronunciation for '{clean_word(word)}'...")
                pronunciation = get_pronunciation(word)
                
                if pronunciation:
                    vocab_item['pronunciation'] = pronunciation
                    words_added += 1
                else:
                    words_failed += 1
                
                # Rate limiting
                time.sleep(delay)
        
        # Process supplementary vocabulary
        if 'transcript' in episode and 'supplementaryVocabulary' in episode['transcript']:
            for vocab_item in episode['transcript']['supplementaryVocabulary']:
                total_words += 1
                word = vocab_item.get('word', '')
                
                # Skip if already has pronunciation
                if 'pronunciation' in vocab_item and vocab_item['pronunciation']:
                    words_with_pronunciation += 1
                    print(f"  ⏭️  '{clean_word(word)}' already has pronunciation")
                    continue
                
                # Fetch pronunciation
                print(f"  🔍 Fetching pronunciation for '{clean_word(word)}'...")
                pronunciation = get_pronunciation(word)
                
                if pronunciation:
                    vocab_item['pronunciation'] = pronunciation
                    words_added += 1
                else:
                    words_failed += 1
                
                # Rate limiting
                time.sleep(delay)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total vocabulary words: {total_words}")
    print(f"Already had pronunciation: {words_with_pronunciation}")
    print(f"Pronunciations added: {words_added}")
    print(f"Failed to fetch: {words_failed}")
    print(f"{'='*60}\n")
    
    # Save if not dry run
    if not dry_run:
        backup_path = json_path.with_suffix('.json.backup')
        print(f"💾 Creating backup: {backup_path}")
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saving updated JSON: {json_path}")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ File updated successfully!")
    else:
        print("ℹ️  DRY RUN - No changes saved. Run with --live to save changes.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Add IPA pronunciations to vocabulary items')
    parser.add_argument('--live', action='store_true', help='Actually save changes (default is dry-run)')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between API calls in seconds (default: 0.5)')
    parser.add_argument('--file', type=str, default='src/data/all-episodes-mapped.json', 
                       help='Path to JSON file (default: src/data/all-episodes-mapped.json)')
    
    args = parser.parse_args()
    
    json_path = Path(args.file)
    
    if not json_path.exists():
        print(f"❌ Error: File not found: {json_path}")
        return
    
    add_pronunciations_to_json(json_path, dry_run=not args.live, delay=args.delay)

if __name__ == '__main__':
    main()
