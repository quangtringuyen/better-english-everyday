import { useState, useEffect } from 'react';

interface SupportModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const SupportModal = ({ isOpen, onClose }: SupportModalProps) => {
    const [supportLink, setSupportLink] = useState('https://buymeacoffee.com/quangtringuyen');
    const [supportImage, setSupportImage] = useState('/support-me.JPG');

    // Load settings from localStorage
    useEffect(() => {
        const savedLink = localStorage.getItem('supportLink');
        const savedImage = localStorage.getItem('supportImage');

        if (savedLink) setSupportLink(savedLink);
        if (savedImage) setSupportImage(savedImage);
    }, []);

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="support-popup" onClick={e => e.stopPropagation()}>
                <div className="support-header">
                    <h3>☕ Support Me</h3>
                    <button className="modal-close" onClick={onClose}>&times;</button>
                </div>

                <div className="support-body">
                    <div className="support-content">
                        <p className="support-message">
                            If you enjoy this app, consider buying me a coffee! 😊
                        </p>

                        {/* QR Code Image */}
                        <div className="support-image-container">
                            <img
                                src={supportImage}
                                alt="Support Me QR Code"
                                className="support-qr-image"
                            />
                        </div>

                        {/* OR Separator */}
                        <div className="or-separator">
                            <span>OR</span>
                        </div>

                        {/* Link Button */}
                        <a
                            href={supportLink}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="support-link-button"
                        >
                            ☕ Buy Me a Coffee
                        </a>
                        <p className="support-url">{supportLink}</p>
                    </div>
                </div>
            </div>

            <style>{`
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.8);
                    z-index: 2500;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    backdrop-filter: blur(5px);
                }

                .support-popup {
                    width: 90%;
                    max-width: 450px;
                    background: linear-gradient(135deg, #1DB954 0%, #179443 100%);
                    border-radius: 16px;
                    overflow: hidden;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
                }

                .support-header {
                    padding: 1rem 1.5rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid rgba(255,255,255,0.2);
                    background: rgba(0,0,0,0.1);
                }

                .support-header h3 {
                    margin: 0;
                    font-size: 1.1rem;
                    color: white;
                }

                .support-body {
                    padding: 2rem;
                    background: transparent;
                }

                .support-content {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }

                .support-message {
                    margin: 0 0 1.5rem 0;
                    color: white;
                    font-size: 1rem;
                }

                .support-message-large {
                    margin: 0 0 2rem 0;
                    color: var(--text-secondary);
                    font-size: 1.1rem;
                    line-height: 1.6;
                }

                .support-image-container {
                    width: 100%;
                    max-width: 350px;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                }

                .support-qr-image {
                    width: 100%;
                    height: auto;
                    display: block;
                }

                .or-separator {
                    width: 100%;
                    display: flex;
                    align-items: center;
                    margin: 2rem 0;
                    gap: 1rem;
                }

                .or-separator::before,
                .or-separator::after {
                    content: '';
                    flex: 1;
                    height: 1px;
                    background: rgba(255,255,255,0.3);
                }

                .or-separator span {
                    color: white;
                    font-weight: 600;
                    font-size: 0.9rem;
                }

                .support-link-button {
                    display: inline-block;
                    padding: 1rem 2.5rem;
                    background: #1DB954;
                    color: white;
                    text-decoration: none;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 1.15rem;
                    box-shadow: 0 6px 20px rgba(29, 185, 84, 0.4);
                    transition: all 0.3s ease;
                    margin-bottom: 1rem;
                }

                .support-link-button:hover {
                    background: #179443;
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(29, 185, 84, 0.5);
                }

                .support-url {
                    margin: 0;
                    font-size: 0.85rem;
                    color: rgba(255,255,255,0.8);
                    word-break: break-all;
                }

                @media (max-width: 480px) {
                    .support-popup {
                        width: 95%;
                        max-width: none;
                    }

                    .support-body {
                        padding: 1.5rem;
                    }

                    .support-link-button {
                        padding: 0.9rem 2rem;
                        font-size: 1rem;
                    }
                }
            `}</style>
        </div>
    );
};
