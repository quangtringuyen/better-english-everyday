import type { Episode } from '../types';

/**
 * YouTube EnglishPod Episodes
 * 
 * To add episodes from YouTube:
 * 1. Watch the video and expand the description
 * 2. Copy the Conversation, Key Vocabulary, and Supplementary Vocabulary
 * 3. Add a new episode object below following the template
 * 
 * Template:
 * {
 *   id: [next number],
 *   videoId: "[YouTube video ID]",
 *   title: "[Video title]",
 *   level: "[Elementary/Intermediate/Advanced]",
 *   description: "[Brief description]",
 *   audioUrl: "https://www.youtube.com/watch?v=[videoId]",
 *   transcript: {
 *     dialogue: [
 *       { speaker: "A", text: "..." },
 *       { speaker: "B", text: "..." }
 *     ],
 *     vocabulary: [
 *       { 
 *         word: "example", 
 *         definition: "...",
 *         category: "noun",
 *         subcategory: "common noun, singular"
 *       }
 *     ],
 *     supplementaryVocabulary: [
 *       { 
 *         word: "additional", 
 *         definition: "...",
 *         category: "adjective",
 *         subcategory: "descriptive"
 *       }
 *     ]
 *   }
 * }
 */

export const youtubeEpisodes: Episode[] = [
    {
        id: 1,
        videoId: "z2jPY6CJZjs",
        title: "EnglishPod 1 - Elementary - Difficult Customer",
        level: "Elementary",
        description: "Learn how to handle a difficult customer at a restaurant. Practice ordering food and dealing with complaints.",
        audioUrl: "https://www.youtube.com/watch?v=z2jPY6CJZjs",
        transcript: {
            dialogue: [
                { speaker: "A", text: "Good evening. My name is Fabio. I'll be your waiter for tonight. May I take your order?" },
                { speaker: "B", text: "No, I'm still working on it. This menu is not even in English. What's good here?" },
                { speaker: "A", text: "For you sir, I would recommend spaghetti and meatballs." },
                { speaker: "B", text: "Does it come with coke and fries?" },
                { speaker: "A", text: "It comes with either soup or salad and a complimentary glass of wine, sir." },
                { speaker: "B", text: "I'll go with the spaghetti and meatballs, salad and the wine." },
                { speaker: "A", text: "Excellent choice. Your order will be ready soon." },
                { speaker: "B", text: "How soon is soon?" },
                { speaker: "A", text: "Twenty minutes?" },
                { speaker: "B", text: "You know what? I'll just go grab a burger across the street." }
            ],
            vocabulary: [
                {
                    word: "recommend",
                    definition: "to suggest something as good or suitable",
                    category: "verb",
                    subcategory: "present simple"
                },
                {
                    word: "complimentary",
                    definition: "given free of charge",
                    category: "adjective",
                    subcategory: "descriptive"
                },
                {
                    word: "go with",
                    definition: "to choose or select",
                    category: "verb",
                    subcategory: "phrasal verb"
                }
            ],
            supplementaryVocabulary: [
                {
                    word: "waiter",
                    definition: "a person who serves food in a restaurant",
                    category: "noun",
                    subcategory: "common noun, singular"
                },
                {
                    word: "menu",
                    definition: "a list of food available in a restaurant",
                    category: "noun",
                    subcategory: "common noun, singular"
                },
                {
                    word: "order",
                    definition: "a request for food or drinks",
                    category: "noun",
                    subcategory: "common noun, singular"
                }
            ]
        }
    },
    // Add more episodes here as you extract them from YouTube
    // Follow the template above
];

// Merge with existing episodes if needed
export { episodes } from './episodes';

// Combined episodes from both sources
export const allEpisodes: Episode[] = [
    ...youtubeEpisodes,
    // You can add episodes from other sources here
];
