import { useState, useRef, useEffect } from 'react';
import type { AudioPlayerState } from '../types';

export const useAudioPlayer = (audioUrl: string) => {
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const [state, setState] = useState<AudioPlayerState>({
        isPlaying: false,
        currentTime: 0,
        duration: 0,
        volume: 1,
        playbackRate: 1,
        isLooping: false,
        isAutoplay: false,
    });

    // Use ref to track autoplay preference preventing dependency cycles
    const isAutoplayRef = useRef(false);

    // Sync ref with state
    useEffect(() => {
        isAutoplayRef.current = state.isAutoplay;
    }, [state.isAutoplay]);

    useEffect(() => {
        const audio = new Audio(audioUrl);
        audioRef.current = audio;

        // Reset state when audio changes
        setState(prev => {
            // Update ref to match current state (preserved from previous)
            isAutoplayRef.current = prev.isAutoplay;

            return {
                isPlaying: prev.isAutoplay, // Start playing if autoplay is on
                currentTime: 0,
                duration: 0,
                volume: 1,
                playbackRate: 1,
                isLooping: false,
                isAutoplay: prev.isAutoplay,
            };
        });

        if (isAutoplayRef.current) {
            audio.play().catch(e => console.log("Autoplay blocked:", e));
        }

        const handleLoadedMetadata = () => {
            setState(prev => ({ ...prev, duration: audio.duration }));
        };

        const handleTimeUpdate = () => {
            setState(prev => ({ ...prev, currentTime: audio.currentTime }));
        };

        const handleEnded = () => {
            setState(prev => ({
                ...prev,
                isPlaying: false,
                currentTime: 0
            }));

            // Trigger auto-next if enabled
            if (isAutoplayRef.current) {
                // Dispatch custom event for auto-next
                window.dispatchEvent(new CustomEvent('audioEnded'));
            }
        };

        audio.addEventListener('loadedmetadata', handleLoadedMetadata);
        audio.addEventListener('timeupdate', handleTimeUpdate);
        audio.addEventListener('ended', handleEnded);

        return () => {
            audio.pause();
            audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
            audio.removeEventListener('timeupdate', handleTimeUpdate);
            audio.removeEventListener('ended', handleEnded);
        };
    }, [audioUrl]); // Remove state.isAutoplay from deps

    const togglePlay = () => {
        if (!audioRef.current) return;

        if (state.isPlaying) {
            audioRef.current.pause();
        } else {
            audioRef.current.play();
        }
        setState(prev => ({ ...prev, isPlaying: !prev.isPlaying }));
    };

    const seek = (time: number) => {
        if (!audioRef.current) return;
        audioRef.current.currentTime = time;
        setState(prev => ({ ...prev, currentTime: time }));
    };

    const skip = (seconds: number) => {
        if (!audioRef.current) return;
        const newTime = Math.max(0, Math.min(state.duration, state.currentTime + seconds));
        seek(newTime);
    };

    const setVolume = (volume: number) => {
        if (!audioRef.current) return;
        const clampedVolume = Math.max(0, Math.min(1, volume));
        audioRef.current.volume = clampedVolume;
        setState(prev => ({ ...prev, volume: clampedVolume }));
    };

    const setPlaybackRate = (rate: number) => {
        if (!audioRef.current) return;
        audioRef.current.playbackRate = rate;
        setState(prev => ({ ...prev, playbackRate: rate }));
    };

    const toggleLoop = () => {
        if (!audioRef.current) return;
        audioRef.current.loop = !state.isLooping;
        setState(prev => ({ ...prev, isLooping: !prev.isLooping }));
    };

    const toggleAutoplay = () => {
        setState(prev => ({ ...prev, isAutoplay: !prev.isAutoplay }));
    };

    const formatTime = (seconds: number): string => {
        if (isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return {
        state,
        togglePlay,
        seek,
        skip,
        setVolume,
        setPlaybackRate,
        toggleLoop,
        toggleAutoplay,
        formatTime,
    };
};
