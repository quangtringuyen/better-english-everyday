# YouTube EnglishPod Data Extraction Guide

## Manual Extraction Process

Since you have the YouTube playlist open, here's how to extract the data:

### Step 1: For Each Video
1. Open the video
2. Click "Show more" in the description
3. Copy the following sections:
   - **Conversation** (dialogue between speakers)
   - **Key Vocabulary** (main vocabulary words)
   - **Supplementary Vocabulary** (additional vocabulary)

### Step 2: Paste into the Template Below

For each video, create an entry in `src/data/youtube-episodes.json` following this structure:

```json
{
  "id": 1,
  "videoId": "z2jPY6CJZjs",
  "title": "EnglishPod 1 - Elementary - Difficult Customer",
  "level": "Elementary",
  "audioUrl": "https://www.youtube.com/watch?v=z2jPY6CJZjs",
  "conversation": [
    {
      "speaker": "A",
      "text": "Good evening. My name is Fabio. I'll be your waiter for tonight. May I take your order?"
    },
    {
      "speaker": "B",
      "text": "No, I'm still working on it. This menu is not even in English. What's good here?"
    }
  ],
  "keyVocabulary": [
    {
      "word": "order",
      "definition": "to ask for food or drinks in a restaurant",
      "category": "verb",
      "subcategory": "present simple"
    },
    {
      "word": "menu",
      "definition": "a list of food available in a restaurant",
      "category": "noun",
      "subcategory": "common noun, singular"
    }
  ],
  "supplementaryVocabulary": [
    {
      "word": "waiter",
      "definition": "a person who serves food in a restaurant",
      "category": "noun",
      "subcategory": "common noun, singular"
    }
  ]
}
```

### Vocabulary Categories

**Categories:**
- `verb` - Action words
- `noun` - Person, place, thing
- `adjective` - Describing words
- `adverb` - Modifies verbs
- `phrase` - Multi-word expression
- `preposition` - Position/relationship words

**Subcategories for Verbs:**
- `present simple`
- `past simple`
- `present continuous`
- `past continuous`
- `present perfect`
- `modal verb`
- `phrasal verb`
- `infinitive`

**Subcategories for Nouns:**
- `common noun, singular`
- `common noun, plural`
- `proper noun`
- `uncountable noun`
- `collective noun`

**Subcategories for Adjectives:**
- `descriptive`
- `comparative`
- `superlative`
- `possessive`

## Playlist Information
- **Playlist URL**: https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi
- **First Video**: https://www.youtube.com/watch?v=z2jPY6CJZjs

## Next Steps
1. Extract data from each video manually
2. Save to `youtube-episodes.json`
3. Run the import script (will be created next)
