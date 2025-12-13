import { useAudioPlayer } from '../hooks/useAudioPlayer';

interface AudioPlayerProps {
    audioUrl: string;
    onNext?: () => void;
    onPrevious?: () => void;
    hasNext?: boolean;
    hasPrevious?: boolean;
}

export const AudioPlayer = ({ audioUrl, onNext, onPrevious, hasNext = true, hasPrevious = true }: AudioPlayerProps) => {
    const {
        state,
        togglePlay,
        seek,
        skip,
        setVolume,
        setPlaybackRate,
        toggleLoop,
        toggleAutoplay,
        formatTime,
    } = useAudioPlayer(audioUrl);

    const handleProgressClick = (e: React.MouseEvent<HTMLDivElement>) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percentage = x / rect.width;
        seek(percentage * state.duration);
    };

    const handleVolumeClick = (e: React.MouseEvent<HTMLDivElement>) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percentage = x / rect.width;
        setVolume(percentage);
    };

    const playbackRates = [0.5, 0.75, 1, 1.25, 1.5, 2];
    const currentRateIndex = playbackRates.indexOf(state.playbackRate);
    const nextRate = playbackRates[(currentRateIndex + 1) % playbackRates.length];

    const handleNext = () => {
        // Enable autoplay before going to next episode
        if (!state.isAutoplay) {
            toggleAutoplay();
        }
        onNext?.();
    };

    const handlePrevious = () => {
        // Enable autoplay before going to previous episode
        if (!state.isAutoplay) {
            toggleAutoplay();
        }
        onPrevious?.();
    };

    return (
        <div className="audio-player">
            {/* Progress Bar - Top */}
            <div className="audio-progress-container">
                <span className="time-current">{formatTime(state.currentTime)}</span>
                <div className="audio-progress" onClick={handleProgressClick}>
                    <div
                        className="audio-progress-bar"
                        style={{ width: `${(state.currentTime / state.duration) * 100 || 0}%` }}
                    ></div>
                </div>
                <span className="time-duration">{formatTime(state.duration)}</span>
            </div>

            {/* Main Controls - Center */}
            <div className="audio-controls">
                {/* Loop Button */}
                <button
                    className={`control-button secondary-action ${state.isLooping ? 'active' : ''}`}
                    onClick={toggleLoop}
                    title="Loop"
                >
                    <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"><path d="M17 2l4 4-4 4"></path><path d="M3 11v-1a4 4 0 0 1 4-4h14"></path><path d="M7 22l-4-4 4-4"></path><path d="M21 13v1a4 4 0 0 0-4 4H3"></path></svg>
                </button>

                {/* Previous Episode */}
                <button
                    className="control-button"
                    onClick={handlePrevious}
                    disabled={!hasPrevious}
                    title="Previous Episode"
                >
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                        <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"></path>
                    </svg>
                </button>

                <button className="control-button" onClick={() => skip(-10)} title="Rewind 10s">
                    {/* Skip Backward Icon */}
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M11 18V6l-8.5 6 8.5 6zm.5-6l8.5 6V6l-8.5 6z"></path></svg>
                </button>

                {/* Play/Pause */}
                <button className="control-button play-button" onClick={togglePlay}>
                    {state.isPlaying ? (
                        <svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor">
                            <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"></path>
                        </svg>
                    ) : (
                        <svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor">
                            <path d="M8 5v14l11-7z"></path>
                        </svg>
                    )}
                </button>

                <button className="control-button" onClick={() => skip(10)} title="Forward 10s">
                    {/* Skip Forward Icon */}
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"></path></svg>
                </button>

                {/* Next Episode - Manual navigation */}
                <button
                    className="control-button"
                    onClick={handleNext}
                    disabled={!hasNext}
                    title="Next Episode"
                >
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                        <path d="M6 18l8.5-6L6 6v12zm10-12v12h2V6h-2z"></path>
                    </svg>
                </button>

                <button
                    className={`control-button secondary-action`}
                    onClick={() => setPlaybackRate(nextRate)}
                    title={`Speed: ${state.playbackRate}x`}
                >
                    <span style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>{state.playbackRate}x</span>
                </button>
            </div>

            {/* Volume & Auto-Next - Bottom Row */}
            <div className="audio-settings" style={{ justifyContent: 'space-between', display: 'flex', alignItems: 'center', padding: '0 1rem' }}>
                <div className="volume-control">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"></path></svg>
                    <div className="volume-slider" onClick={handleVolumeClick}>
                        <div
                            className="volume-slider-fill"
                            style={{ width: `${state.volume * 100}%` }}
                        />
                    </div>
                </div>

                {/* Auto-Next Toggle - Bottom Right */}
                <div
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                    }}
                >
                    <span style={{
                        fontSize: '0.75rem',
                        color: 'var(--text-secondary)',
                        whiteSpace: 'nowrap'
                    }}>
                        Auto-next
                    </span>
                    <button
                        onClick={toggleAutoplay}
                        title={state.isAutoplay ? "Auto-next: ON (will play next episode when finished)" : "Auto-next: OFF"}
                        style={{
                            width: '44px',
                            height: '22px',
                            borderRadius: '11px',
                            border: 'none',
                            background: state.isAutoplay ? '#1DB954' : '#ccc',
                            position: 'relative',
                            cursor: 'pointer',
                            transition: 'background 0.3s ease',
                            padding: 0,
                            outline: 'none',
                            flexShrink: 0
                        }}
                    >
                        <div
                            style={{
                                width: '18px',
                                height: '18px',
                                borderRadius: '50%',
                                background: 'white',
                                position: 'absolute',
                                top: '2px',
                                left: state.isAutoplay ? '24px' : '2px',
                                transition: 'left 0.3s ease',
                                boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                            }}
                        />
                    </button>
                </div>
            </div>
        </div >
    );
};
