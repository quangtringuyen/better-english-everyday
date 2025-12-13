import type { Theme } from '../types';

interface HeaderProps {
    theme: Theme;
    onThemeChange: (theme: Theme) => void;
    onOpenManual: () => void;
}

export const Header = ({ theme, onThemeChange, onOpenManual }: HeaderProps) => {
    return (
        <header className="header">
            <div className="header-content">
                <h1 className="header-title">
                    <img src="/book-icon.svg" alt="Logo" className="header-logo" /> Better English Everyday
                </h1>

                <button className="manual-button" onClick={onOpenManual}>
                    📖 <span className="manual-text">User Manual Guide</span>
                </button>

                <div className="theme-switcher">
                    <button
                        className={`theme-button ${theme === 'light' ? 'active' : ''}`}
                        onClick={() => onThemeChange('light')}
                        title="Switch to light theme"
                    >
                        ☀️ Light
                    </button>
                    <button
                        className={`theme-button ${theme === 'dark' ? 'active' : ''}`}
                        onClick={() => onThemeChange('dark')}
                        title="Switch to dark theme"
                    >
                        🌙 Dark
                    </button>
                    <button
                        className={`theme-button ${theme === 'system' ? 'active' : ''}`}
                        onClick={() => onThemeChange('system')}
                        title="Use system theme"
                    >
                        💻 System
                    </button>
                </div>
            </div>
        </header>
    );
};
