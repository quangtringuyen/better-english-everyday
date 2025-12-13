import type { Episode } from '../types';
import { AudioPlayer } from './AudioPlayer';
import { Transcript } from './Transcript';

interface EpisodeDetailProps {
    episode: Episode | null;
    onNext?: () => void;
    onPrevious?: () => void;
    hasNext?: boolean;
    hasPrevious?: boolean;
    isFavorite?: boolean;
    onToggleFavorite?: () => void;
    onOpenFlashcards?: () => void;
}

export const EpisodeDetail = ({ episode, onNext, onPrevious, hasNext, hasPrevious, isFavorite, onToggleFavorite, onOpenFlashcards }: EpisodeDetailProps) => {
    if (!episode) {
        return (
            <div className="episode-detail-container">
                <div className="empty-state">
                    <div className="empty-state-icon">🎧</div>
                    <h2 className="empty-state-title">Select an Episode</h2>
                    <p className="empty-state-description">
                        Choose an episode from the list to start learning English!
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="episode-detail-container" style={{ height: '100%' }}>
            <div className="episode-fixed-header">
                {/* Episode Header */}
                <div className="episode-detail-header" style={{ padding: '0 0.25rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                        <div className="episode-detail-number">Episode {episode.id}</div>
                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                            <button
                                onClick={onOpenFlashcards}
                                style={{
                                    padding: '0.4rem 0.8rem',
                                    backgroundColor: '#1DB954',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '20px',
                                    cursor: 'pointer',
                                    fontWeight: 600,
                                    fontSize: '0.8rem',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.4rem',
                                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                                    whiteSpace: 'nowrap'
                                }}
                            >
                                🎴 Practice Vocabulary
                            </button>
                            <button
                                onClick={onToggleFavorite}
                                style={{
                                    background: 'none',
                                    border: 'none',
                                    cursor: 'pointer',
                                    fontSize: '1.5rem',
                                    lineHeight: 1,
                                    padding: '0.25rem',
                                    borderRadius: '50%',
                                    transition: 'transform 0.2s',
                                    transform: isFavorite ? 'scale(1.1)' : 'scale(1)'
                                }}
                                title={isFavorite ? "Remove from Favorites" : "Add to Favorites"}
                            >
                                {isFavorite ? '💚' : '🤍'}
                            </button>
                        </div>
                    </div>
                    <h2 className="episode-detail-title">{episode.title}</h2>
                    <p className="episode-detail-description">{episode.description}</p>
                </div>

                {/* Audio Player - Fixed in Header */}
                <AudioPlayer
                    audioUrl={`${import.meta.env.VITE_AUDIO_BASE_URL || ''}${episode.audioUrl}`}
                    onNext={onNext}
                    onPrevious={onPrevious}
                    hasNext={hasNext}
                    hasPrevious={hasPrevious}
                />
            </div>

            <div className="episode-scroll-content">
                {/* Transcript & Vocabulary */}
                <Transcript transcript={episode.transcript} />
            </div>
        </div>
    );
};
