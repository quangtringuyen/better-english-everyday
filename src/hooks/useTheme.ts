import { useState, useEffect } from 'react';
import type { Theme } from '../types';

export const useTheme = () => {
    const [theme, setTheme] = useState<Theme>(() => {
        const savedTheme = localStorage.getItem('theme') as Theme;
        return savedTheme || 'system';
    });

    useEffect(() => {
        const root = document.documentElement;

        const applyTheme = (selectedTheme: Theme) => {
            if (selectedTheme === 'system') {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
            } else {
                root.setAttribute('data-theme', selectedTheme);
            }
        };

        applyTheme(theme);
        localStorage.setItem('theme', theme);

        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleChange = () => {
            if (theme === 'system') {
                applyTheme('system');
            }
        };

        mediaQuery.addEventListener('change', handleChange);
        return () => mediaQuery.removeEventListener('change', handleChange);
    }, [theme]);

    return { theme, setTheme };
};
