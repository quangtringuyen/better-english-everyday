export interface Episode {
  id: number;
  originalId?: number;
  videoId?: string;
  title: string;
  level: string;
  folder: string; // Category folder (Entry_01, Entry_02, etc.)
  description: string;
  audioUrl: string;
  transcript: {
    dialogue: DialogueLine[];
    vocabulary: VocabularyItem[];
    supplementaryVocabulary?: VocabularyItem[];
  };
}

export interface DialogueLine {
  speaker: string;
  text: string;
}

export type VocabularyCategory =
  | 'verb'
  | 'noun'
  | 'adjective'
  | 'adverb'
  | 'phrase'
  | 'preposition'
  | 'conjunction'
  | 'pronoun'
  | 'interjection';

export type VerbSubcategory =
  | 'present simple'
  | 'past simple'
  | 'present continuous'
  | 'past continuous'
  | 'present perfect'
  | 'past perfect'
  | 'future simple'
  | 'modal verb'
  | 'phrasal verb'
  | 'infinitive'
  | 'gerund'
  | 'imperative';

export type NounSubcategory =
  | 'common noun, singular'
  | 'common noun, plural'
  | 'proper noun'
  | 'uncountable noun'
  | 'collective noun'
  | 'abstract noun'
  | 'concrete noun';

export type AdjectiveSubcategory =
  | 'descriptive'
  | 'comparative'
  | 'superlative'
  | 'possessive'
  | 'demonstrative'
  | 'quantitative'
  | 'interrogative';

export type VocabularySubcategory =
  | VerbSubcategory
  | NounSubcategory
  | AdjectiveSubcategory
  | string;

export interface VocabularyItem {
  word: string;
  definition: string;
  category?: VocabularyCategory;
  subcategory?: VocabularySubcategory;
  example?: string;
  pronunciation?: string; // US IPA pronunciation
}

export type Theme = 'light' | 'dark' | 'system';

export interface AudioPlayerState {
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  playbackRate: number;
  isLooping: boolean;
  isAutoplay: boolean;
}
