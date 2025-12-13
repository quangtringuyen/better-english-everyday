# YouTube EnglishPod Data Extraction - Complete Guide

## 🎯 Overview

This guide will help you extract conversation and vocabulary data from the YouTube EnglishPod playlist and integrate it into the application with proper grammatical categorization.

**Playlist URL**: https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi

## 📋 Step-by-Step Process

### Step 1: Manual Extraction from YouTube

For each video in the playlist:

1. **Open the video** in YouTube
2. **Click "Show more"** in the description to expand it
3. **Copy the following sections**:
   - Video title and level (Elementary/Intermediate/Advanced)
   - **Conversation** (dialogue between speakers A, B, C, etc.)
   - **Key Vocabulary** (main vocabulary words with definitions)
   - **Supplementary Vocabulary** (additional vocabulary words)

### Step 2: Categorize Vocabulary

For each vocabulary word, determine:

#### **Category** (Main word type):
- `verb` - Action words (run, eat, speak)
- `noun` - Person, place, thing (waiter, menu, restaurant)
- `adjective` - Describing words (good, difficult, complimentary)
- `adverb` - Modifies verbs (quickly, well, carefully)
- `phrase` - Multi-word expressions (go with, take care of)
- `preposition` - Position/relationship (in, on, at, with)
- `conjunction` - Connecting words (and, but, or)
- `pronoun` - Replaces nouns (I, you, he, she, it)

#### **Subcategory** (Specific classification):

**For Verbs**:
- `present simple` - I eat, he eats
- `past simple` - I ate, he ate
- `present continuous` - I am eating
- `past continuous` - I was eating
- `present perfect` - I have eaten
- `past perfect` - I had eaten
- `future simple` - I will eat
- `modal verb` - can, should, must, would
- `phrasal verb` - give up, look after, go with
- `infinitive` - to eat, to go
- `gerund` - eating, going (verb as noun)
- `imperative` - Eat! Go! (commands)

**For Nouns**:
- `common noun, singular` - waiter, menu, order
- `common noun, plural` - waiters, menus, orders
- `proper noun` - Fabio, McDonald's, New York
- `uncountable noun` - water, rice, information
- `collective noun` - team, family, group
- `abstract noun` - happiness, freedom, love
- `concrete noun` - table, chair, food

**For Adjectives**:
- `descriptive` - good, difficult, complimentary
- `comparative` - better, more difficult
- `superlative` - best, most difficult
- `possessive` - my, your, his, her
- `demonstrative` - this, that, these, those
- `quantitative` - many, few, several
- `interrogative` - which, what, whose

### Step 3: Format the Data

Add each episode to `src/data/youtube-episodes.ts`:

```typescript
{
  id: 1,
  videoId: "z2jPY6CJZjs",
  title: "EnglishPod 1 - Elementary - Difficult Customer",
  level: "Elementary",
  description: "Learn how to handle a difficult customer at a restaurant.",
  audioUrl: "https://www.youtube.com/watch?v=z2jPY6CJZjs",
  transcript: {
    dialogue: [
      { speaker: "A", text: "Good evening. My name is Fabio..." },
      { speaker: "B", text: "No, I'm still working on it..." }
    ],
    vocabulary: [
      {
        word: "recommend",
        definition: "to suggest something as good or suitable",
        category: "verb",
        subcategory: "present simple",
        example: "I recommend the spaghetti."
      }
    ],
    supplementaryVocabulary: [
      {
        word: "waiter",
        definition: "a person who serves food in a restaurant",
        category: "noun",
        subcategory: "common noun, singular"
      }
    ]
  }
}
```

## 🎨 Visual Features

The application will display:

- **Color-coded badges** for word categories:
  - 🔵 Blue = Verbs
  - 🟢 Green = Nouns
  - 🟣 Purple = Adjectives
  - 🟡 Yellow = Adverbs
  - 🌸 Pink = Phrases
  - 🔷 Indigo = Prepositions

- **Subcategory labels** in italics below each word
- **Example sentences** in highlighted boxes
- **Separate sections** for Key Vocabulary and Supplementary Vocabulary

## 📝 Quick Reference Template

```
EPISODE [NUMBER]
Title: [Copy from YouTube]
Level: [Elementary/Intermediate/Advanced]
Video ID: [Last part of YouTube URL]

CONVERSATION:
A: [First line]
B: [Response]
[Continue...]

KEY VOCABULARY:
1. [word] - [definition]
   Category: [verb/noun/adjective/etc]
   Subcategory: [specific type]
   Example: [optional]

SUPPLEMENTARY VOCABULARY:
1. [word] - [definition]
   Category: [verb/noun/adjective/etc]
   Subcategory: [specific type]
```

## 🚀 After Extraction

Once you've added episodes to `youtube-episodes.ts`, the application will automatically:

1. Display them in the episode list
2. Show color-coded vocabulary badges
3. Organize vocabulary by category
4. Display supplementary vocabulary separately
5. Link to the YouTube video for audio playback

## 💡 Tips

- Start with 5-10 episodes to test the system
- Be consistent with categorization
- Add examples for difficult words
- Use the exact speaker labels from YouTube (A, B, C, etc.)
- Keep definitions concise and clear

## 🔗 Resources

- **Playlist**: https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi
- **First Video**: https://www.youtube.com/watch?v=z2jPY6CJZjs
- **Data File**: `src/data/youtube-episodes.ts`
- **Types File**: `src/types.ts`

---

**Happy Learning! 🎓**
