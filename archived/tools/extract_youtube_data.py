#!/usr/bin/env python3
"""
YouTube EnglishPod Data Extractor

This script extracts conversation and vocabulary data from YouTube EnglishPod videos
and formats them into TypeScript data structures.

Usage:
    python extract_youtube_data.py <youtube_url>
    python extract_youtube_data.py --playlist <playlist_url>
"""

import re
import json
import sys
from typing import Dict, List, Optional
from html import unescape


def parse_vocabulary_item(text: str) -> Dict[str, str]:
    """
    Parse a vocabulary item like:
    "Grab (principle verb, present simple): Get quickly"
    
    Returns dict with word, category, subcategory, and definition
    """
    # Pattern: word (category, subcategory): definition
    # or: word (category): definition
    # or: word: definition
    
    result = {
        'word': '',
        'definition': '',
        'category': None,
        'subcategory': None
    }
    
    # Split by colon to separate word/categories from definition
    if ':' in text:
        parts = text.split(':', 1)
        word_part = parts[0].strip()
        result['definition'] = parts[1].strip()
        
        # Check for categories in parentheses
        if '(' in word_part and ')' in word_part:
            word = word_part[:word_part.index('(')].strip()
            categories = word_part[word_part.index('(')+1:word_part.index(')')].strip()
            
            result['word'] = word
            
            # Parse categories
            cat_parts = [c.strip() for c in categories.split(',')]
            
            # Map common category names
            category_map = {
                'principle verb': 'verb',
                'verb': 'verb',
                'phrase': 'phrase',
                'adjective': 'adjective',
                'common noun': 'noun',
                'noun': 'noun',
                'adverb': 'adverb',
                'preposition': 'preposition'
            }
            
            for cat in cat_parts:
                cat_lower = cat.lower()
                if cat_lower in category_map:
                    result['category'] = category_map[cat_lower]
                elif any(verb_type in cat_lower for verb_type in ['present simple', 'past simple', 'present continuous', 'modal', 'phrasal']):
                    result['subcategory'] = cat_lower
                elif any(noun_type in cat_lower for noun_type in ['singular', 'plural', 'uncountable']):
                    result['subcategory'] = cat_lower
                else:
                    # If not recognized as category, might be subcategory
                    if result['category'] and not result['subcategory']:
                        result['subcategory'] = cat_lower
        else:
            result['word'] = word_part
    else:
        result['word'] = text.strip()
    
    return result


def parse_description(html_content: str) -> Dict:
    """
    Parse the YouTube video description HTML content
    """
    # Remove HTML tags but keep structure
    text = unescape(html_content)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '\n', text)
    
    # Clean up whitespace
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    result = {
        'title': '',
        'level': '',
        'conversation': [],
        'keyVocabulary': [],
        'supplementaryVocabulary': []
    }
    
    current_section = None
    
    for i, line in enumerate(lines):
        # Extract title and level
        if i == 0 and 'EnglishPod' in line:
            result['title'] = line.strip()
            # Extract level
            if 'Elementary' in line:
                result['level'] = 'Elementary'
            elif 'Intermediate' in line:
                result['level'] = 'Intermediate'
            elif 'Advanced' in line:
                result['level'] = 'Advanced'
            continue
        
        # Detect sections
        if line.lower() == 'conversation':
            current_section = 'conversation'
            continue
        elif 'key vocabulary' in line.lower():
            current_section = 'key_vocabulary'
            continue
        elif 'supplementary vocabulary' in line.lower():
            current_section = 'supplementary_vocabulary'
            continue
        
        # Parse content based on current section
        if current_section == 'conversation':
            # Match dialogue lines like "A:  Good evening..."
            match = re.match(r'^([A-Z]):\s*(.+)$', line)
            if match:
                speaker = match.group(1)
                text = match.group(2).strip()
                result['conversation'].append({
                    'speaker': speaker,
                    'text': text
                })
        
        elif current_section == 'key_vocabulary':
            if line and not line.lower().startswith('key vocabulary'):
                vocab = parse_vocabulary_item(line)
                if vocab['word']:
                    result['keyVocabulary'].append(vocab)
        
        elif current_section == 'supplementary_vocabulary':
            if line and not line.lower().startswith('supplementary'):
                vocab = parse_vocabulary_item(line)
                if vocab['word']:
                    result['supplementaryVocabulary'].append(vocab)
    
    return result


def generate_typescript_episode(data: Dict, video_id: str, episode_num: int) -> str:
    """
    Generate TypeScript code for an episode
    """
    
    def escape_quotes(text: str) -> str:
        """Escape double quotes and backslashes for TypeScript strings"""
        return text.replace('\\', '\\\\').replace('"', '\\"')
    
    # Format dialogue
    dialogue_lines = []
    for line in data['conversation']:
        speaker = escape_quotes(line["speaker"])
        text = escape_quotes(line["text"])
        dialogue_lines.append(f'      {{ speaker: "{speaker}", text: "{text}" }}')
    dialogue_str = ',\n'.join(dialogue_lines)
    
    # Format key vocabulary
    vocab_lines = []
    for item in data['keyVocabulary']:
        word = escape_quotes(item["word"])
        definition = escape_quotes(item["definition"])
        vocab_obj = f'      {{\n        word: "{word}",\n        definition: "{definition}"'
        if item['category']:
            vocab_obj += f',\n        category: "{escape_quotes(item["category"])}"'
        if item['subcategory']:
            vocab_obj += f',\n        subcategory: "{escape_quotes(item["subcategory"])}"'
        vocab_obj += '\n      }'
        vocab_lines.append(vocab_obj)
    vocab_str = ',\n'.join(vocab_lines)
    
    # Format supplementary vocabulary
    supp_vocab_lines = []
    for item in data['supplementaryVocabulary']:
        word = escape_quotes(item["word"])
        definition = escape_quotes(item["definition"])
        vocab_obj = f'      {{\n        word: "{word}",\n        definition: "{definition}"'
        if item['category']:
            vocab_obj += f',\n        category: "{escape_quotes(item["category"])}"'
        if item['subcategory']:
            vocab_obj += f',\n        subcategory: "{escape_quotes(item["subcategory"])}"'
        vocab_obj += '\n      }'
        supp_vocab_lines.append(vocab_obj)
    supp_vocab_str = ',\n'.join(supp_vocab_lines)
    
    # Generate description
    description = f"Learn {data['title'].split(' - ')[-1].lower() if ' - ' in data['title'] else 'English'} through this lesson."
    description = escape_quotes(description)
    title = escape_quotes(data['title'])
    level = escape_quotes(data['level'])
    
    ts_code = f'''  {{
    id: {episode_num},
    videoId: "{video_id}",
    title: "{title}",
    level: "{level}",
    description: "{description}",
    audioUrl: "https://www.youtube.com/watch?v={video_id}",
    transcript: {{
      dialogue: [
{dialogue_str}
      ],
      vocabulary: [
{vocab_str}
      ],
      supplementaryVocabulary: [
{supp_vocab_str}
      ]
    }}
  }}'''
    
    return ts_code


def main():
    """
    Main function - for now, demonstrates parsing with the provided example
    """
    
    # Example HTML from the user
    example_html = '''<div id="expanded" class="style-scope ytd-text-inline-expander"><yt-attributed-string class="style-scope ytd-text-inline-expander"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" dir="auto"><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">EnglishPod 1 - Elementary - Difficult Customer

Conversation 
A:  Good evening. My name is Fabio. I'll be your waiter for tonight. May I take your order?
B:  No, I'm still working on it. This menu isn't even in English. What's good here?
A:  For you sir, I would recommend  spaghetti and meatballs.
B:  Does it come with coke and fries?
A:  It comes with either soup or salad and a complimentary glass of wine, sir.
B:  I'll go with the spaghetti and meatballs, salad and the wine.
A:  Excellent choice. Your order will be ready soon.
B:  How soon is soon?
A:  Twenty minutes?
B:  You know what? I'll just go grab a burger across the street.

Key Vocabulary 
</span><ul class="yt-core-attributed-string__list-group" dir="ltr"><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Grab (principle verb, present simple): Get quickly
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Go with (phrase): To choose, pick
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Would recommend: Suggest
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Complimentary (Adjective): Free
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Still working on (phrase): Not yet completed, need more time
</span></li></ul><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">
Supplementary Vocabulary 
</span><ul class="yt-core-attributed-string__list-group" dir="ltr"><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Impatient: Uncomfortable waiting, wanting to go
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Fast food (phrase): Food prepared and served quickly
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Waitress (common noun, singular): Female server at a restaurant or bar
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Fancy (Adjective): Nice, expensive, up-scale
</span></li><li><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">Casual (Adjective): Relaxed, not dressy</span></li></ul></span></yt-attributed-string><yt-formatted-string disable-attributed-string="" class="style-scope ytd-text-inline-expander" disable-upgrade="" hidden=""></yt-formatted-string></div>'''
    
    # Parse the data
    data = parse_description(example_html)
    
    # Generate TypeScript code
    ts_code = generate_typescript_episode(data, "z2jPY6CJZjs", 1)
    
    print("Parsed Data:")
    print(json.dumps(data, indent=2))
    print("\n" + "="*80 + "\n")
    print("TypeScript Episode Code:")
    print(ts_code)
    
    # Save to file
    with open('extracted_episode.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    with open('extracted_episode.ts', 'w') as f:
        f.write(ts_code)
    
    print("\n" + "="*80)
    print("✅ Data saved to:")
    print("  - extracted_episode.json (JSON format)")
    print("  - extracted_episode.ts (TypeScript format)")


if __name__ == '__main__':
    main()
