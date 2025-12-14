import { useState, useMemo, useEffect } from 'react';
import { Header } from './components/Header';
import { EpisodeList } from './components/EpisodeList';
import { EpisodeDetail } from './components/EpisodeDetail';

import { UserManualModal } from './components/UserManualModal';
import { FlashcardModal } from './components/FlashcardModal';
import { SupportModal } from './components/SupportModal';
import { useTheme } from './hooks/useTheme';
import { AdminPanel } from './components/admin/AdminPanel';
import allEpisodesMapped from './data/all-episodes-mapped.json';
import './index.css';
import './layout-fixes.css';
import './mobile-menu-fix.css';


// Use the mapped episodes data directly (already has clean titles and proper structure)
// const allEpisodes = allEpisodesMapped; -> Moved to state

function App() {
  const { theme, setTheme } = useTheme();
  // Ensure we use number for ID, initialize with first cleaned episode ID
  const [allEpisodes, setAllEpisodes] = useState<any[]>(allEpisodesMapped);

  // Initialize from URL or default
  const [selectedEpisodeId, setSelectedEpisodeId] = useState<number>(() => {
    const params = new URLSearchParams(window.location.search);
    const idParam = params.get('id');
    if (idParam) {
      const id = parseInt(idParam, 10);
      if (allEpisodesMapped.some(e => e.id === id)) {
        return id;
      }
    }
    return allEpisodesMapped[0]?.id || 1;
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [showMobileEpisodeList, setShowMobileEpisodeList] = useState(false);
  const [showManual, setShowManual] = useState(false);
  const [showFlashcards, setShowFlashcards] = useState(false);
  const [showSupport, setShowSupport] = useState(false);
  // Persist Admin Mode
  const [isAdminMode, setIsAdminMode] = useState(() => localStorage.getItem('app_mode') === 'admin');

  useEffect(() => {
    localStorage.setItem('app_mode', isAdminMode ? 'admin' : 'app');
  }, [isAdminMode]);

  const [completedEpisodes, setCompletedEpisodes] = useState<number[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [totalVisits, setTotalVisits] = useState<number | null>(null);

  // Handle browser back/forward navigation
  useEffect(() => {
    const handlePopState = () => {
      const params = new URLSearchParams(window.location.search);
      const idParam = params.get('id');
      if (idParam) {
        const id = parseInt(idParam, 10);
        // Only update if valid ID is found
        if (allEpisodesMapped.some(e => e.id === id)) {
          setSelectedEpisodeId(id);
        }
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Public Visitor Counter (Session based)
  useEffect(() => {
    const hasVisited = sessionStorage.getItem('has_counted_visit');
    if (!hasVisited) {
      // Increment the counter
      fetch('https://api.countapi.xyz/hit/better-english-everyday/visits')
        .then(res => res.json())
        .then(data => {
          setTotalVisits(data.value);
          sessionStorage.setItem('has_counted_visit', 'true');
        })
        .catch(e => console.error('Counter error', e));
    } else {
      // Just fetch current count without incrementing
      fetch('https://api.countapi.xyz/get/better-english-everyday/visits')
        .then(res => res.json())
        .then(data => setTotalVisits(data.value))
        .catch(e => console.error('Counter get error', e));
    }
  }, []);

  // Update URL when episode changes (Sync State -> URL)
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const currentParamId = params.get('id');

    // Only push if the URL is different to avoid duplicate history entries/loops
    if (currentParamId !== String(selectedEpisodeId)) {
      const newUrl = `${window.location.pathname}?id=${selectedEpisodeId}`;
      window.history.pushState({ id: selectedEpisodeId }, '', newUrl);
    }
  }, [selectedEpisodeId]);

  // Load state from localStorage
  useEffect(() => {
    try {
      const savedCompleted = localStorage.getItem('completedEpisodes');
      if (savedCompleted) setCompletedEpisodes(JSON.parse(savedCompleted));

      const savedFavorites = localStorage.getItem('favorites');
      if (savedFavorites) setFavorites(JSON.parse(savedFavorites));
    } catch (e) {
      console.error('Failed to parse local storage', e);
    }
  }, []);

  // Toggle favorite
  const handleToggleFavorite = (id: number) => {
    setFavorites(prev => {
      const newFavorites = prev.includes(id)
        ? prev.filter(favId => favId !== id)
        : [...prev, id];
      localStorage.setItem('favorites', JSON.stringify(newFavorites));
      return newFavorites;
    });
  };

  // Filter episodes based on search
  const displayedEpisodes = useMemo(() => {
    if (!searchQuery.trim()) return allEpisodes;

    const query = searchQuery.toLowerCase();
    return allEpisodes.filter(
      (episode: any) =>
        episode.title.toLowerCase().includes(query) ||
        episode.description?.toLowerCase().includes(query) ||
        episode.level?.toLowerCase().includes(query)
    );
  }, [searchQuery]);

  // Get selected episode
  const selectedEpisode = useMemo(() => {
    return allEpisodes.find((ep: any) => ep.id === selectedEpisodeId) || allEpisodes[0];
  }, [selectedEpisodeId]);

  // Handle episode selection (close mobile list after selection)
  const handleSelectEpisode = (id: number) => {
    setSelectedEpisodeId(id);
    setShowMobileEpisodeList(false);
  };

  // Navigation functions
  const currentIndex = useMemo(() => {
    return allEpisodes.findIndex((ep: any) => ep.id === selectedEpisodeId);
  }, [selectedEpisodeId, allEpisodes]);

  const hasNext = currentIndex < allEpisodes.length - 1;
  const hasPrevious = currentIndex > 0;

  const handleNext = () => {
    if (hasNext) {
      const nextEpisode = allEpisodes[currentIndex + 1];
      setSelectedEpisodeId(nextEpisode.id);
    }
  };

  const handlePrevious = () => {
    if (hasPrevious) {
      const prevEpisode = allEpisodes[currentIndex - 1];
      setSelectedEpisodeId(prevEpisode.id);
    }
  };

  // Handle auto-next episode and marks as completed
  useEffect(() => {
    const handleAudioEnded = () => {
      // Find current episode index
      const currentIndex = allEpisodes.findIndex((ep: any) => ep.id === selectedEpisodeId);

      // Mark as completed
      if (!completedEpisodes.includes(selectedEpisodeId)) {
        const newCompleted = [...completedEpisodes, selectedEpisodeId];
        setCompletedEpisodes(newCompleted);
        localStorage.setItem('completedEpisodes', JSON.stringify(newCompleted));
      }

      // If there's a next episode, select it
      if (currentIndex !== -1 && currentIndex < allEpisodes.length - 1) {
        const nextEpisode = allEpisodes[currentIndex + 1];
        setSelectedEpisodeId(nextEpisode.id);
      }
    };

    window.addEventListener('audioEnded', handleAudioEnded);

    return () => {
      window.removeEventListener('audioEnded', handleAudioEnded);
    };
  }, [selectedEpisodeId, allEpisodes, completedEpisodes]);

  if (isAdminMode) {
    return (
      <AdminPanel
        episodes={allEpisodes}
        onUpdateEpisodes={setAllEpisodes}
        onExit={() => setIsAdminMode(false)}
      />
    );
  }

  return (
    <div className="app">
      <Header
        theme={theme}
        onThemeChange={setTheme}
        onOpenManual={() => setShowManual(true)}
      />

      <main className="main-content">
        {/* Episode Detail - Left side on desktop */}
        <div className="episode-detail">
          <EpisodeDetail
            episode={selectedEpisode}
            onNext={handleNext}
            onPrevious={handlePrevious}
            hasNext={hasNext}
            hasPrevious={hasPrevious}
            isFavorite={favorites.includes(selectedEpisodeId)}
            onToggleFavorite={() => handleToggleFavorite(selectedEpisodeId)}
            onOpenFlashcards={() => setShowFlashcards(true)}
          />
        </div>

        {/* Desktop Episode List Sidebar - Right side on desktop */}
        <div className="episode-detail">
          <div className="episode-list-container">
            <EpisodeList
              episodes={displayedEpisodes}
              selectedEpisodeId={selectedEpisodeId}
              onSelectEpisode={handleSelectEpisode}
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              completedEpisodes={completedEpisodes}
              favorites={favorites}
            />
          </div>
        </div>

        {/* Backdrop overlay for mobile menu */}
        {showMobileEpisodeList && (
          <div
            className="mobile-menu-backdrop"
            onClick={() => setShowMobileEpisodeList(false)}
          />
        )}

        {/* Mobile slide-over menu */}
        <div
          className={`mobile-playlist-wrapper ${showMobileEpisodeList ? 'show' : ''}`}
          style={{
            position: 'fixed',
            top: 0,
            right: showMobileEpisodeList ? 0 : '-100%',
            width: '85vw',
            maxWidth: '350px',
            minWidth: '300px',
            height: '100vh',
            zIndex: 2000,
            backgroundColor: theme === 'dark' ? '#121212' : '#ffffff',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden', // Changed from 'auto' to 'hidden'
            transition: 'right 0.3s ease-out',
            boxShadow: '-5px 0 20px rgba(0, 0, 0, 0.3)'
          }}
        >
          <EpisodeList
            episodes={displayedEpisodes}
            selectedEpisodeId={selectedEpisodeId}
            onSelectEpisode={handleSelectEpisode}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            completedEpisodes={completedEpisodes}
            favorites={favorites}
          />
        </div>
      </main>

      {/* Mobile Episode Toggle Button */}
      <button
        className="mobile-episode-toggle"
        onClick={() => setShowMobileEpisodeList(!showMobileEpisodeList)}
        aria-label={showMobileEpisodeList ? 'Close menu' : 'Open menu'}
      >
        {showMobileEpisodeList ? '✕' : '☰'}
      </button>

      <footer className="app-footer" style={{
        flexShrink: 0,
        backgroundColor: 'var(--bg-secondary)',
        borderTop: '1px solid var(--border-color)',
        padding: '0.5rem',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '0.4rem',
        zIndex: 90, // Below mobile menu (2000) and toggle (101)
        boxShadow: '0 -2px 10px rgba(0,0,0,0.1)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
          <button
            onClick={() => setShowSupport(true)}
            style={{
              background: '#1DB954',
              color: 'white',
              border: 'none',
              padding: '0.4rem 0.8rem',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              fontSize: '0.8rem',
              fontWeight: 600,
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.3rem',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = '#179443'}
            onMouseLeave={(e) => e.currentTarget.style.background = '#1DB954'}
          >
            ☕ Buy me a coffee
          </button>
          <button
            onClick={() => setIsAdminMode(true)}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.75rem',
              color: 'var(--text-secondary)',
              padding: '0.2rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.2rem',
              opacity: 0.7
            }}
            title="Admin Access"
          >
            🔒
          </button>

          <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', opacity: 0.8, marginLeft: '0.5rem', borderLeft: '1px solid var(--border-color)', paddingLeft: '0.5rem' }}>
            Visits: {totalVisits !== null ? totalVisits.toLocaleString() : '...'}
          </span>
        </div>
        <p style={{ margin: 0, fontSize: '0.7rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
          © {new Date().getFullYear()} Better English Everyday. All rights reserved. Developed by Tri Nguyen.
        </p>
      </footer>
      <UserManualModal isOpen={showManual} onClose={() => setShowManual(false)} />
      <SupportModal isOpen={showSupport} onClose={() => setShowSupport(false)} />
      <FlashcardModal
        isOpen={showFlashcards}
        onClose={() => setShowFlashcards(false)}
        vocabulary={selectedEpisode.transcript?.vocabulary || []}
      />
    </div >
  );
}

export default App;
