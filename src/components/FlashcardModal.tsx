import React, { useState, useEffect } from 'react';
import type { VocabularyItem } from '../types';

interface FlashcardModalProps {
    isOpen: boolean;
    onClose: () => void;
    vocabulary: VocabularyItem[];
}

export const FlashcardModal = ({ isOpen, onClose, vocabulary }: FlashcardModalProps) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isFlipped, setIsFlipped] = useState(false);

    useEffect(() => {
        // Reset when modal opens or vocabulary changes
        if (isOpen) {
            setCurrentIndex(0);
            setIsFlipped(false);
        }
    }, [isOpen, vocabulary]);

    if (!isOpen || vocabulary.length === 0) return null;

    const currentItem = vocabulary[currentIndex];

    const handleNext = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsFlipped(false);
        setCurrentIndex(prev => (prev + 1) % vocabulary.length);
    };

    const handlePrev = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsFlipped(false);
        setCurrentIndex(prev => (prev - 1 + vocabulary.length) % vocabulary.length);
    };

    const handleFlip = () => {
        setIsFlipped(!isFlipped);
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="flashcard-container" onClick={e => e.stopPropagation()}>
                <div className="flashcard-header">
                    <h3>Vocabulary Practice ({currentIndex + 1}/{vocabulary.length})</h3>
                    <button className="modal-close" onClick={onClose}>&times;</button>
                </div>

                <div className="flashcard-body">
                    <div
                        className={`flashcard ${isFlipped ? 'flipped' : ''}`}
                        onClick={handleFlip}
                    >
                        <div className="flashcard-inner">
                            <div className="flashcard-front">
                                <span className="category-badge">{currentItem.category || 'Word'}</span>
                                <h2>{currentItem.word}</h2>
                                {currentItem.pronunciation && (
                                    <div className="pronunciation">/{currentItem.pronunciation}/</div>
                                )}
                                <p className="tap-hint">👆 Tap to flip</p>
                            </div>
                            <div className="flashcard-back">
                                <h3>Definition</h3>
                                <p>{currentItem.definition}</p>
                                {/* We don't have example in VocabularyItem type yet usually, but checking Transcript logic... */}
                                {/* Actually Transcript component renders it, let's assume definition implies example text sometimes or check type */}
                            </div>
                        </div>
                    </div>

                    <div className="flashcard-controls">
                        <button className="nav-btn" onClick={handlePrev}>← Prev</button>
                        <button className="nav-btn primary" onClick={handleNext}>Next →</button>
                    </div>
                </div>
            </div>

            <style>{`
                .modal-overlay {
                    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                    background: rgba(0,0,0,0.8); z-index: 2500;
                    display: flex; align-items: center; justify-content: center;
                    backdrop-filter: blur(5px);
                }
                .flashcard-container {
                    width: 90%; max-width: 500px;
                    background: var(--bg-primary); border-radius: 16px;
                    overflow: hidden;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
                }
                .flashcard-header {
                    padding: 1rem 1.5rem;
                    display: flex; justify-content: space-between; align-items: center;
                    border-bottom: 1px solid var(--border-color);
                    background: var(--bg-secondary);
                }
                .flashcard-header h3 { margin: 0; font-size: 1.1rem; color: var(--text-primary); }
                .flashcard-body {
                    padding: 2rem;
                    display: flex; flex-direction: column; align-items: center;
                    background: var(--bg-primary); 
                    min-height: 400px;
                }
                .flashcard {
                    width: 100%; height: 300px;
                    perspective: 1000px;
                    cursor: pointer;
                    margin-bottom: 2rem;
                }
                .flashcard-inner {
                    position: relative; width: 100%; height: 100%;
                    text-align: center;
                    transition: transform 0.6s;
                    transform-style: preserve-3d;
                    background: linear-gradient(135deg, #1DB954 0%, #179443 100%);
                    color: white;
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3);
                }
                .flashcard.flipped .flashcard-inner {
                    transform: rotateY(180deg);
                    background: white;
                    color: #333;
                }
                /* Dark mode support for back of card */
                @media (prefers-color-scheme: dark) {
                    .flashcard.flipped .flashcard-inner {
                        background: #333;
                        color: #f0f0f0;
                    }
                }
                
                .flashcard-front, .flashcard-back {
                    position: absolute; width: 100%; height: 100%;
                    -webkit-backface-visibility: hidden;
                    backface-visibility: hidden;
                    display: flex; flex-direction: column;
                    align-items: center; justify-content: center;
                    padding: 2rem;
                    box-sizing: border-box;
                }
                .flashcard-back {
                    transform: rotateY(180deg);
                }
                
                .flashcard-front h2 { font-size: 2.5rem; margin: 1rem 0; }
                .pronunciation { 
                    font-family: serif; font-size: 1.2rem; 
                    opacity: 0.9; margin-bottom: 2rem;
                    background: rgba(255,255,255,0.2);
                    padding: 0.2rem 1rem; border-radius: 20px;
                }
                .category-badge {
                    position: absolute; top: 1rem; right: 1rem;
                    background: rgba(0,0,0,0.2);
                    padding: 0.25rem 0.75rem; border-radius: 99px;
                    font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
                }
                .tap-hint {
                    position: absolute; bottom: 1rem;
                    font-size: 0.8rem; opacity: 0.7;
                }

                .flashcard-controls {
                    display: flex; gap: 1rem; width: 100%;
                }
                .nav-btn {
                    flex: 1; padding: 0.8rem;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    background: var(--bg-secondary);
                    color: var(--text-primary);
                    font-weight: 600; cursor: pointer;
                    transition: all 0.2s;
                }
                .nav-btn:hover { background: var(--border-color); }
                .nav-btn.primary {
                    background: #1DB954; color: white; border: none;
                }
                .nav-btn.primary:hover { background: #179443; }
            `}</style>
        </div>
    );
};
