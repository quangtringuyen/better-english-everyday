
interface UserManualModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const UserManualModal = ({ isOpen, onClose }: UserManualModalProps) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>📚 Podcast for Newbie - User Manual Guide</h2>
                    <button className="modal-close" onClick={onClose}>&times;</button>
                </div>
                <div className="modal-body">
                    <p className="intro">Welcome to <strong>Podcast for Newbie</strong>, your interactive English learning companion! This guide will help you make the most of all features.</p>

                    <section>
                        <h3>🚀 Getting Started</h3>
                        <p><strong>First Time Setup:</strong></p>
                        <ol>
                            <li>Open the App in your browser.</li>
                            <li>Browse the episode list grouped by difficulty.</li>
                            <li>Click any episode to start learning.</li>
                        </ol>

                        <p><strong>Difficulty Levels:</strong></p>
                        <ul>
                            <li>🟢 <strong>Elementary</strong> (41 eps) - Basic conversations</li>
                            <li>🔵 <strong>Basic</strong> (100 eps) - Beginner topics</li>
                            <li>🟡 <strong>Pre-Intermediate</strong> (100 eps) - Building foundations</li>
                            <li>🟠 <strong>Lower Intermediate</strong> (63 eps) - Developing skills</li>
                            <li>🟣 <strong>Intermediate</strong> - Intermediate topics</li>
                            <li>🔴 <strong>Advanced</strong> (9 eps) - Complex discussions</li>
                        </ul>
                    </section>

                    <section>
                        <h3>🧭 Navigating the App</h3>
                        <ul>
                            <li><strong>Header:</strong> Search bar, theme toggle (☀️ Light / 🌙 Dark).</li>
                            <li><strong>Sidebar:</strong> Full list of episodes. On mobile, use the ☰ hamburger menu.</li>
                            <li><strong>Detail View:</strong> Contains transcript, vocabulary, and audio player.</li>
                        </ul>
                        <p><strong>Tip:</strong> You can search for topics like "airport" or "restaurant" in the search bar!</p>
                    </section>

                    <section>
                        <h3>🎵 Audio Player Controls</h3>
                        <p>Located at the bottom of the content area:</p>
                        <div className="control-grid">
                            <div className="control-item">▶️ <strong>Play/Pause:</strong> Start or stop audio.</div>
                            <div className="control-item">⏪ ⏩ <strong>Skip:</strong> Jump +/- 10 seconds.</div>
                            <div className="control-item">⏮️ ⏭️ <strong>Prev/Next:</strong> Switch episodes.</div>
                            <div className="control-item">⏱️ <strong>Speed:</strong> Adjust playback (0.5x - 2x).</div>
                            <div className="control-item">🔁 <strong>Auto-Next:</strong> Toggle switch to play next episode automatically.</div>
                        </div>
                    </section>

                    <section>
                        <h3>📚 Learning Features</h3>

                        <h4>1. Transcript & Vocabulary</h4>
                        <p>The core learning area. Click the 👁️ eye icon to show/hide if needed.</p>

                        <h4>2. Key Vocabulary Badges</h4>
                        <p>Words are color-coded for instant recognition:</p>
                        <div className="badge-grid">
                            <span className="kb phrase">🌸 Phrase</span>
                            <span className="kb noun">🟢 Noun</span>
                            <span className="kb verb">🔵 Verb</span>
                            <span className="kb adj">🟣 Adjective</span>
                            <span className="kb adv">🟡 Adverb</span>
                        </div>

                        <h4>3. IPA Pronunciation</h4>
                        <p>Look for the orange badges next to words (e.g., <span className="ipa-badge">/həˈləʊ/</span>). These show the correct US pronunciation.</p>
                    </section>

                    <section>
                        <h3>💡 Tips for Success</h3>
                        <ul>
                            <li><strong>Read First:</strong> Skim the transcript and vocabulary before listening.</li>
                            <li><strong>Listen Active:</strong> Try to listen without reading, then check the text.</li>
                            <li><strong>Shadowing:</strong> Repeat after the speaker to practice pronunciation.</li>
                            <li><strong>Consistency:</strong> Aim for 1 episode per day!</li>
                        </ul>
                    </section>

                    <section>
                        <h3>❓ Troubleshooting</h3>
                        <ul>
                            <li><strong>Audio won't play?</strong> Check internet or refresh the page.</li>
                            <li><strong>Can't see menu on mobile?</strong> Tap the ☰ icon in top-left.</li>
                            <li><strong>Auto-next stops?</strong> Ensure the toggle is Green (ON).</li>
                        </ul>
                    </section>

                    <footer className="manual-footer">
                        <p><em>Happy Learning! 📚🎧✨</em></p>
                    </footer>
                </div>
            </div>
            <style>{`
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: rgba(0, 0, 0, 0.75);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 3000;
                    backdrop-filter: blur(4px);
                    animation: fadeIn 0.2s ease-out;
                }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                .modal-content {
                    background-color: var(--bg-secondary);
                    color: var(--text-primary);
                    width: 90%;
                    max-width: 800px; /* Wider for reading */
                    max-height: 90vh;
                    border-radius: 12px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                    display: flex;
                    flex-direction: column;
                    border: 1px solid var(--border-color);
                }
                .modal-header {
                    padding: 1.5rem;
                    border-bottom: 1px solid var(--border-color);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: var(--bg-primary);
                    border-radius: 12px 12px 0 0;
                }
                .modal-header h2 {
                    margin: 0;
                    font-size: 1.5rem;
                    color: #22c55e;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 2rem;
                    line-height: 1;
                    color: var(--text-secondary);
                    cursor: pointer;
                    padding: 0 0.5rem;
                    transition: color 0.2s;
                }
                .modal-close:hover {
                    color: var(--text-primary);
                }
                .modal-body {
                    padding: 2rem;
                    overflow-y: auto;
                    font-size: 1rem;
                    line-height: 1.6;
                }
                .modal-body section {
                    margin-bottom: 2.5rem;
                }
                .modal-body h3 {
                    margin-top: 0;
                    margin-bottom: 1rem;
                    color: var(--text-primary);
                    font-size: 1.25rem;
                    border-bottom: 2px solid #22c55e;
                    display: inline-block;
                    padding-bottom: 0.25rem;
                }
                .modal-body h4 {
                    margin: 1.5rem 0 0.5rem;
                    color: var(--text-primary);
                    font-size: 1.1rem;
                }
                .modal-body ul, .modal-body ol {
                    padding-left: 1.5rem;
                    margin: 0.5rem 0;
                }
                .modal-body li {
                    margin-bottom: 0.5rem;
                    color: var(--text-secondary);
                }
                .modal-body p {
                    color: var(--text-secondary);
                    margin-bottom: 1rem;
                }
                .modal-footer {
                    margin-top: 2rem;
                    text-align: center;
                    color: #22c55e;
                    font-size: 1.1rem;
                    border-top: 1px solid var(--border-color);
                    padding-top: 1rem;
                }
                
                /* Custom styles for guide elements */
                .badge-grid {
                    display: flex;
                    gap: 0.5rem;
                    flex-wrap: wrap;
                    margin: 1rem 0;
                }
                .kb {
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                    font-weight: 500;
                    color: #fff;
                }
                .kb.phrase { background-color: #db2777; }
                .kb.noun { background-color: #16a34a; }
                .kb.verb { background-color: #2563eb; }
                .kb.adj { background-color: #9333ea; }
                .kb.adv { background-color: #ca8a04; }

                .ipa-badge {
                    color: #c2410c;
                    background-color: #fed7aa;
                    border: 1px solid #fdba74;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: serif;
                    font-weight: 500;
                }

                .control-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 1rem;
                    margin: 1rem 0;
                }
                .control-item {
                    background: var(--bg-primary);
                    padding: 0.75rem;
                    border-radius: 8px;
                    border: 1px solid var(--border-color);
                    font-size: 0.9rem;
                    color: var(--text-secondary);
                }
                .intro {
                    font-size: 1.1rem;
                    border-left: 4px solid #22c55e;
                    padding-left: 1rem;
                }

                @media (max-width: 600px) {
                    .modal-body { padding: 1rem; }
                    .modal-header h2 { font-size: 1.25rem; }
                }
            `}</style>
        </div>
    );
};
