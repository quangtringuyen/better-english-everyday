import { useState, useMemo } from 'react';

interface Episode {
    id: number;
    title: string;
    folder?: string;
    description: string;
}

interface EpisodeListProps {
    episodes: Episode[];
    selectedEpisodeId: number | null;
    onSelectEpisode: (id: number) => void;
    searchQuery: string;
    onSearchChange: (query: string) => void;
    completedEpisodes?: number[];
    favorites?: number[];
}

export const EpisodeList = ({ episodes, selectedEpisodeId, onSelectEpisode, searchQuery, onSearchChange, completedEpisodes = [], favorites = [] }: EpisodeListProps) => {
    const [selectedCategory, setSelectedCategory] = useState<string>('All');

    // Get unique categories from folder property
    const categories = useMemo(() => {
        const folders = episodes.map(ep => ep.folder).filter((f): f is string => Boolean(f));
        const cats = Array.from(new Set(folders));

        // Define level order - Basic through Lower Intermediate are beginner levels
        const levelOrder = ['Elementary', 'Basic', 'Pre-Intermediate', 'Lower Intermediate', 'Intermediate', 'Advanced', 'Upper Intermediate'];

        // Sort by level order
        const sorted = cats.sort((a, b) => {
            const indexA = levelOrder.indexOf(a);
            const indexB = levelOrder.indexOf(b);

            // If both are in levelOrder, sort by their position
            if (indexA !== -1 && indexB !== -1) {
                return indexA - indexB;
            }
            // If only one is in levelOrder, it comes first
            if (indexA !== -1) return -1;
            if (indexB !== -1) return 1;
            // Otherwise, sort alphabetically
            return a.localeCompare(b);
        });

        return ['All', ...sorted];
    }, [episodes]);

    const filteredEpisodes = useMemo(() => {
        return episodes.filter(ep => {
            const matchesCategory = selectedCategory === 'Favorites'
                ? favorites.includes(ep.id)
                : selectedCategory === 'All' || ep.folder === selectedCategory;
            const matchesSearch = ep.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                ep.id.toString().includes(searchQuery);
            return matchesCategory && matchesSearch;
        });
    }, [episodes, selectedCategory, searchQuery, favorites]);

    const formatCategoryName = (cat: string) => {
        if (!cat) return '';
        if (cat === 'All') return 'All Levels';
        // Remove underscores and capitalize
        return cat.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        ).join(' ');
    };



    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            width: '100%',
            height: '100%'
        }}>
            {/* Search Bar */}
            <div style={{
                padding: '0.75rem',
                borderBottom: '1px solid #e0e0e0',
                backgroundColor: '#f8f8f8',
                flexShrink: 0
            }}>
                <input
                    type="text"
                    placeholder="Search episodes..."
                    value={searchQuery}
                    onChange={(e) => onSearchChange(e.target.value)}
                    style={{
                        width: '100%',
                        padding: '0.5rem 1rem',
                        borderRadius: '8px',
                        border: '1px solid #d0d0d0',
                        backgroundColor: '#ffffff',
                        color: '#000000',
                        fontSize: '14px',
                        boxSizing: 'border-box'
                    }}
                />
            </div>

            {/* Category Menu - Grouped by Level */}
            <div style={{
                padding: '0.75rem',
                borderBottom: '1px solid #e0e0e0',
                backgroundColor: '#fafafa',
                flexShrink: 0
            }}>
                {/* All button */}
                <button
                    onClick={() => setSelectedCategory('All')}
                    style={{
                        width: '100%',
                        padding: '0.6rem',
                        marginBottom: '0.5rem',
                        borderRadius: '8px',
                        border: selectedCategory === 'All' ? '2px solid #1DB954' : '1px solid #d0d0d0',
                        backgroundColor: selectedCategory === 'All' ? '#1DB954' : '#ffffff',
                        color: selectedCategory === 'All' ? '#000000' : '#666666',
                        fontSize: '0.85rem',
                        fontWeight: selectedCategory === 'All' ? 700 : 600,
                        cursor: 'pointer',
                        textAlign: 'left'
                    }}
                >
                    📚 All Levels
                </button>

                {/* Favorites button */}
                <button
                    onClick={() => setSelectedCategory('Favorites')}
                    style={{
                        width: '100%',
                        padding: '0.6rem',
                        marginBottom: '0.5rem',
                        borderRadius: '8px',
                        border: selectedCategory === 'Favorites' ? '2px solid #1DB954' : '1px solid #d0d0d0',
                        backgroundColor: selectedCategory === 'Favorites' ? '#1DB954' : '#ffffff',
                        color: selectedCategory === 'Favorites' ? '#ffffff' : '#666666',
                        fontSize: '0.85rem',
                        fontWeight: selectedCategory === 'Favorites' ? 700 : 600,
                        cursor: 'pointer',
                        textAlign: 'left'
                    }}
                >
                    💚 Favorites ({favorites.length})
                </button>

                {/* Compact Category Filter - All in one row */}
                <div style={{ marginBottom: '0.75rem' }}>
                    <div style={{
                        fontSize: '0.65rem',
                        color: 'var(--text-tertiary)',
                        marginBottom: '0.4rem',
                        fontWeight: 500,
                        fontStyle: 'italic'
                    }}>
                        💡 Learning Path: Follow the numbers 1️⃣ → 7️⃣
                    </div>
                    <div style={{
                        display: 'flex',
                        flexWrap: 'wrap',
                        gap: '0.4rem'
                    }}>
                        {(() => {
                            // Define the learning sequence order
                            const learningOrder = [
                                'Elementary',
                                'Basic',
                                'Pre-Intermediate',
                                'Lower Intermediate',
                                'Intermediate',
                                'Advanced',
                                'Upper Intermediate'
                            ];

                            // Filter and sort categories based on learning order
                            const sortedCategories = categories
                                .filter(cat => cat !== 'All')
                                .sort((a, b) => {
                                    const indexA = learningOrder.indexOf(a);
                                    const indexB = learningOrder.indexOf(b);
                                    return indexA - indexB;
                                });

                            return sortedCategories.map((cat, index) => {
                                // Determine emoji based on category
                                let emoji = '';
                                if (cat === 'Elementary') emoji = '🟢';
                                else if (cat === 'Basic') emoji = '🔵';
                                else if (cat === 'Pre-Intermediate') emoji = '🟡';
                                else if (cat === 'Lower Intermediate') emoji = '🟠';
                                else if (cat === 'Intermediate') emoji = '🟣';
                                else if (cat === 'Upper Intermediate') emoji = '🟣';
                                else if (cat === 'Advanced') emoji = '🔴';

                                // Number for sequence
                                const number = index + 1;

                                return (
                                    <button
                                        key={cat}
                                        onClick={() => setSelectedCategory(cat)}
                                        style={{
                                            padding: '0.35rem 0.65rem',
                                            borderRadius: '16px',
                                            border: selectedCategory === cat ? '2px solid #1DB954' : '1px solid var(--border-color)',
                                            backgroundColor: selectedCategory === cat ? '#1DB954' : 'var(--bg-secondary)',
                                            color: selectedCategory === cat ? '#000000' : 'var(--text-secondary)',
                                            fontSize: '0.7rem',
                                            fontWeight: selectedCategory === cat ? 700 : 500,
                                            cursor: 'pointer',
                                            whiteSpace: 'nowrap',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '0.3rem'
                                        }}
                                    >
                                        <span style={{ fontWeight: 600 }}>{number}.</span>
                                        <span>{emoji}</span>
                                        <span>{formatCategoryName(cat)}</span>
                                    </button>
                                );
                            });
                        })()}
                    </div>
                </div>

            </div>

            {/* Episode List */}
            <div style={{
                flex: 1,
                overflowY: 'auto',
                padding: '0.5rem',
                backgroundColor: '#ffffff'
            }}>
                {filteredEpisodes.map((episode) => (
                    <div
                        key={episode.id}
                        onClick={() => onSelectEpisode(episode.id)}
                        style={{
                            padding: '0.75rem',
                            marginBottom: '0.5rem',
                            borderRadius: '8px',
                            border: selectedEpisodeId === episode.id ? '2px solid #1DB954' : '1px solid #e0e0e0',
                            backgroundColor: selectedEpisodeId === episode.id ? '#1DB954' : '#f5f5f5',
                            cursor: 'pointer',
                            transition: 'all 0.2s'
                        }}
                    >
                        <div style={{
                            fontSize: '0.75rem',
                            color: selectedEpisodeId === episode.id ? '#000000' : '#666666',
                            marginBottom: '0.25rem',
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                        }}>
                            <span>Episode {episode.id}</span>
                            {completedEpisodes.includes(episode.id) && (
                                <span title="Completed" style={{ fontSize: '0.9rem' }}>✅</span>
                            )}
                        </div>
                        <div style={{
                            fontSize: '0.875rem',
                            color: selectedEpisodeId === episode.id ? '#000000' : '#333333',
                            lineHeight: 1.3
                        }}>
                            {episode.title}
                        </div>
                    </div>
                ))}
                {filteredEpisodes.length === 0 && (
                    <div style={{
                        textAlign: 'center',
                        padding: '2rem',
                        color: '#999999'
                    }}>
                        No episodes found
                    </div>
                )}
            </div>
        </div>
    );
};
