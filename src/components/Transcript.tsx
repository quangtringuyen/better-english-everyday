import { useState } from 'react';
import type { Episode } from '../types';

interface TranscriptProps {
    transcript: Episode['transcript'];
}

export const Transcript = ({ transcript }: TranscriptProps) => {
    const [isVisible, setIsVisible] = useState(true); // Show by default

    const getCategoryBadgeColor = (category?: string) => {
        const isDark = document.documentElement.classList.contains('dark');

        switch (category?.toLowerCase()) {
            case 'verb':
                return { backgroundColor: isDark ? '#1e3a8a' : '#dbeafe', color: isDark ? '#93c5fd' : '#1e40af' };
            case 'noun':
                return { backgroundColor: isDark ? '#14532d' : '#dcfce7', color: isDark ? '#86efac' : '#15803d' };
            case 'adjective':
                return { backgroundColor: isDark ? '#581c87' : '#f3e8ff', color: isDark ? '#d8b4fe' : '#7e22ce' };
            case 'adverb':
                return { backgroundColor: isDark ? '#713f12' : '#fef9c3', color: isDark ? '#fde047' : '#a16207' };
            case 'phrase':
                return { backgroundColor: isDark ? '#831843' : '#fce7f3', color: isDark ? '#f9a8d4' : '#be185d' };
            case 'preposition':
                return { backgroundColor: isDark ? '#312e81' : '#e0e7ff', color: isDark ? '#a5b4fc' : '#4f46e5' };
            default:
                return { backgroundColor: isDark ? '#374151' : '#f3f4f6', color: isDark ? '#d1d5db' : '#1f2937' };
        }
    };

    const getSubcategoryBadgeColor = (subcategory?: string) => {
        const isDark = document.documentElement.classList.contains('dark');

        if (!subcategory) {
            return { backgroundColor: isDark ? '#374151' : '#f3f4f6', color: isDark ? '#d1d5db' : '#6b7280' };
        }

        const lower = subcategory.toLowerCase();

        // Noun types
        if (lower.includes('singular') || lower.includes('plural')) {
            return { backgroundColor: isDark ? '#064e3b' : '#d1fae5', color: isDark ? '#6ee7b7' : '#047857' };
        }
        if (lower.includes('common') || lower.includes('proper')) {
            return { backgroundColor: isDark ? '#134e4a' : '#ccfbf1', color: isDark ? '#5eead4' : '#0f766e' };
        }

        // Verb types
        if (lower.includes('transitive') || lower.includes('intransitive')) {
            return { backgroundColor: isDark ? '#0c4a6e' : '#e0f2fe', color: isDark ? '#7dd3fc' : '#0369a1' };
        }
        if (lower.includes('modal') || lower.includes('auxiliary')) {
            return { backgroundColor: isDark ? '#164e63' : '#cffafe', color: isDark ? '#67e8f9' : '#0e7490' };
        }

        // Adjective/Adverb types
        if (lower.includes('comparative') || lower.includes('superlative')) {
            return { backgroundColor: isDark ? '#5b21b6' : '#ede9fe', color: isDark ? '#c4b5fd' : '#6d28d9' };
        }

        // Default
        return { backgroundColor: isDark ? '#475569' : '#e2e8f0', color: isDark ? '#cbd5e1' : '#475569' };
    };

    // Parse word to extract clean word and categories
    const parseWord = (wordWithCategory: string) => {
        // Match pattern: "word (category)" or "word (category, subcategory)"
        const match = wordWithCategory.match(/^(.+?)\s*\(([^)]+)\)$/);

        if (!match) {
            return { word: wordWithCategory, category: undefined, subcategory: undefined };
        }

        const cleanWord = match[1].trim();
        const categoriesText = match[2].trim();

        // Split by comma to separate category and subcategory
        const parts = categoriesText.split(',').map(p => p.trim());

        if (parts.length === 1) {
            // Only category
            return { word: cleanWord, category: parts[0], subcategory: undefined };
        } else {
            // Category and subcategory
            return { word: cleanWord, category: parts[0], subcategory: parts.slice(1).join(', ') };
        }
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            flex: 1,
            overflow: 'hidden'
        }}>
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '0.75rem 1.5rem',
                backgroundColor: 'var(--bg-secondary)',
                borderRadius: '0.75rem 0.75rem 0 0',
                border: '1px solid var(--border-color)',
                borderBottom: isVisible ? 'none' : '1px solid var(--border-color)'
            }}>
                <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--text-primary)' }}>Transcript</h3>
                <button
                    onClick={() => setIsVisible(!isVisible)}
                    style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: '0.9rem',
                        color: 'var(--text-secondary)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        fontWeight: 500,
                        padding: '0.5rem'
                    }}
                >
                    {isVisible ? '👁️ Hide' : '👁️ Show'}
                </button>
            </div>

            {isVisible && (
                <div className="transcript-content">
                    {/* Dialogue Section */}
                    <div className="transcript-dialogue">
                        <h3>📝 Dialogue</h3>
                        {transcript.dialogue.map((line, index) => (
                            <div key={index} className="dialogue-line">
                                <strong>{line.speaker}:</strong> {line.text}
                            </div>
                        ))}
                    </div>

                    {/* Key Vocabulary Section */}
                    {transcript.vocabulary.length > 0 && (
                        <div className="transcript-vocabulary">
                            <h3>📚 Key Vocabulary</h3>
                            {transcript.vocabulary.map((item, index) => {
                                const parsed = parseWord(item.word);
                                return (
                                    <div key={index} className="vocabulary-item">
                                        <div className="vocabulary-word-header">
                                            <span className="vocabulary-word">{parsed.word}</span>
                                            {item.pronunciation && <span style={{ fontSize: '0.875rem', color: 'white', fontStyle: 'normal', fontFamily: '"Segoe UI", Arial, sans-serif', fontWeight: '500', marginLeft: '10px', padding: '2px 8px', backgroundColor: '#3b82f6', borderRadius: '4px', whiteSpace: 'nowrap' }}>/{item.pronunciation}/</span>}
                                            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                                                {parsed.category && (
                                                    <span className="vocabulary-badge" style={{ ...getCategoryBadgeColor(parsed.category), padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '500' }}>
                                                        {parsed.category}
                                                    </span>
                                                )}
                                                {parsed.subcategory && (
                                                    <span className="vocabulary-badge" style={{ ...getSubcategoryBadgeColor(parsed.subcategory), padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '500' }}>
                                                        {parsed.subcategory}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="vocabulary-definition">{item.definition}</div>
                                        {item.example && (
                                            <div className="vocabulary-example">
                                                <em>Example: {item.example}</em>
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    )}

                    {/* Supplementary Vocabulary Section */}
                    {transcript.supplementaryVocabulary && transcript.supplementaryVocabulary.length > 0 && (
                        <div className="transcript-vocabulary">
                            <h3>📖 Supplementary Vocabulary</h3>
                            {transcript.supplementaryVocabulary.map((item, index) => {
                                const parsed = parseWord(item.word);
                                return (
                                    <div key={index} className="vocabulary-item">
                                        <div className="vocabulary-word-header">
                                            <span className="vocabulary-word">{parsed.word}</span>
                                            {item.pronunciation && <span style={{ fontSize: '0.875rem', color: 'white', fontStyle: 'normal', fontFamily: '"Segoe UI", Arial, sans-serif', fontWeight: '500', marginLeft: '10px', padding: '2px 8px', backgroundColor: '#3b82f6', borderRadius: '4px', whiteSpace: 'nowrap' }}>/{item.pronunciation}/</span>}
                                            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                                                {parsed.category && (
                                                    <span className="vocabulary-badge" style={{ ...getCategoryBadgeColor(parsed.category), padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '500' }}>
                                                        {parsed.category}
                                                    </span>
                                                )}
                                                {parsed.subcategory && (
                                                    <span className="vocabulary-badge" style={{ ...getSubcategoryBadgeColor(parsed.subcategory), padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '500' }}>
                                                        {parsed.subcategory}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="vocabulary-definition">{item.definition}</div>
                                        {item.example && (
                                            <div className="vocabulary-example">
                                                <em>Example: {item.example}</em>
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};
