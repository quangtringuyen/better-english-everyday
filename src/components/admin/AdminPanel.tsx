import { useState, useEffect } from 'react';
import type { Episode } from '../../types';

interface AdminPanelProps {
    episodes: Episode[];
    onUpdateEpisodes: (newEpisodes: Episode[]) => void;
    onExit: () => void;
}

const VisitorLogTable = () => {
    const [logs, setLogs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/resources/visitors.log')
            .then(res => {
                if (!res.ok) throw new Error('No log file');
                return res.text();
            })
            .then(text => {
                const lines = text.trim().split('\n');
                const parsed = lines.map(line => {
                    try {
                        const clean = line.trim().replace(/,$/, '');
                        return JSON.parse(clean);
                    } catch (e) { return null; }
                }).filter(Boolean).reverse().slice(0, 50);
                setLogs(parsed);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, []);

    if (loading) return <div style={{ padding: '1rem' }}>Loading logs...</div>;
    if (logs.length === 0) return <div style={{ padding: '1rem' }}>No logs found yet.</div>;

    return (
        <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', minWidth: '400px', fontSize: '0.85rem', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ background: '#eee', textAlign: 'left' }}>
                        <th style={{ padding: '8px' }}>Time</th>
                        <th style={{ padding: '8px' }}>IP</th>
                        <th style={{ padding: '8px' }}>Path</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.map((log, i) => (
                        <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
                            <td style={{ padding: '8px' }}>{new Date(log.timestamp).toLocaleString()}</td>
                            <td style={{ padding: '8px' }}>{log.ip}</td>
                            <td style={{ padding: '8px' }}>{log.path}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

// Add responsive styles
const adminStyles = `
  @media (max-width: 768px) {
    .admin-panel { padding: 1rem !important; }
    .admin-header { flex-direction: column; align-items: flex-start; gap: 1rem; }
    .admin-header-actions { width: 100%; flex-wrap: wrap; }
    .admin-header-actions button { flex: 1; }
  }
`;

export const AdminPanel = ({ episodes, onUpdateEpisodes, onExit }: AdminPanelProps) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [password, setPassword] = useState('');
    const [editingId, setEditingId] = useState<number | null>(null);
    const [editForm, setEditForm] = useState<Partial<Episode>>({});

    // Support settings state
    const [supportLink, setSupportLink] = useState('https://buymeacoffee.com/quangtringuyen');

    // Password change state
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    // Analytics State
    const [visitCount, setVisitCount] = useState<number | null>(null);
    const [adminIp, setAdminIp] = useState<string>('');

    // Fetch Analytics on mount
    useEffect(() => {
        // Get Visit Count
        fetch('https://api.countapi.xyz/get/better-english-everyday/visits')
            .then(res => res.json())
            .then(data => setVisitCount(data.value))
            .catch(err => console.error('Failed to fetch visits', err));

        // Get Admin IP
        fetch('https://api.ipify.org?format=json')
            .then(res => res.json())
            .then(data => setAdminIp(data.ip))
            .catch(err => console.error('Failed to fetch IP', err));
    }, []);

    // Load support settings from localStorage
    useEffect(() => {
        const savedLink = localStorage.getItem('supportLink');

        if (savedLink) setSupportLink(savedLink);
    }, []);

    // Save support settings
    const handleSaveSupportSettings = () => {
        localStorage.setItem('supportLink', supportLink);
        alert('Support settings saved successfully!');
    };

    // --- NEW: Save JSON to File Functionality ---
    const handleSaveToFile = async () => {
        try {
            // Check if File System Access API is supported (Chrome/Edge/Opera)
            if ('showSaveFilePicker' in window) {
                const handle = await (window as any).showSaveFilePicker({
                    suggestedName: 'all-episodes-mapped.json',
                    types: [{
                        description: 'JSON File',
                        accept: { 'application/json': ['.json'] },
                    }],
                });
                const writable = await handle.createWritable();
                await writable.write(JSON.stringify(episodes, null, 2));
                await writable.close();
                alert('Success! File saved.\n\nChanges are now permanent on your disk.');
            } else {
                // Fallback for Firefox/Safari: Download the file
                handleDownloadJson();
            }
        } catch (err) {
            console.error('Failed to save file:', err);
            // Don't alert if user just cancelled
            if ((err as Error).name !== 'AbortError') {
                alert('Could not write to file directly. Trying download instead...');
                handleDownloadJson();
            }
        }
    };

    const handleDownloadJson = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(episodes, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "all-episodes-mapped.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
        alert('File downloaded!\n\nPlease move this file to "src/data/all-episodes-mapped.json" to persist changes.');
    };
    // --------------------------------------------

    // Get stored password or use default
    const getStoredPassword = () => {
        return localStorage.getItem('adminPassword') || 'admin123';
    };

    // Password login check
    const handleLogin = () => {
        if (password === getStoredPassword()) {
            setIsAuthenticated(true);
        } else {
            alert('Wrong password');
        }
    };

    // Change password
    const handleChangePassword = () => {
        if (!newPassword || !confirmPassword) {
            alert('Please fill in both password fields');
            return;
        }
        if (newPassword !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        if (newPassword.length < 6) {
            alert('Password must be at least 6 characters long');
            return;
        }

        localStorage.setItem('adminPassword', newPassword);
        setNewPassword('');
        setConfirmPassword('');
        alert('Password changed successfully!');
    };

    const handleEdit = (episode: Episode) => {
        setEditingId(episode.id);
        setEditForm({ ...episode });
    };

    const handleSave = () => {
        if (!editingId) return;

        const updatedEpisodes = episodes.map(ep =>
            ep.id === editingId ? { ...ep, ...editForm } as Episode : ep
        );

        onUpdateEpisodes(updatedEpisodes);
        setEditingId(null);
    };


    if (!isAuthenticated) {
        return (
            <div className="admin-login" style={{
                padding: '2rem',
                textAlign: 'center',
                height: '100vh',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                background: '#f0f2f5'
            }}>
                <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
                    <h2 style={{ marginBottom: '1.5rem', color: '#333' }}>Admin Access</h2>
                    <div style={{ marginBottom: '1rem' }}>
                        <input
                            type="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            placeholder="Enter Password"
                            onKeyDown={e => e.key === 'Enter' && handleLogin()}
                            style={{
                                padding: '0.75rem',
                                marginRight: '0.5rem',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                minWidth: '250px'
                            }}
                        />
                    </div>
                    <button
                        onClick={handleLogin}
                        style={{
                            padding: '0.75rem 2rem',
                            background: '#1DB954',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontWeight: 'bold',
                            width: '100%'
                        }}
                    >
                        Login
                    </button>
                    <div style={{ marginTop: '1.5rem' }}>
                        <button onClick={onExit} style={{ background: 'none', border: 'none', color: '#666', textDecoration: 'underline', cursor: 'pointer' }}>
                            ← Back to App
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="admin-panel" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', backgroundColor: '#ffffff', minHeight: '100vh', color: '#000000' }}>
            <style>{adminStyles}</style>
            <div className="admin-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', borderBottom: '1px solid #ddd', paddingBottom: '1rem' }}>
                <h1 style={{ margin: 0, color: '#333' }}>Admin Dashboard</h1>
                <div className="admin-header-actions" style={{ display: 'flex', gap: '1rem' }}>
                    <button
                        onClick={handleSaveToFile}
                        style={{
                            padding: '0.5rem 1rem',
                            background: '#2563eb', // Blue
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontWeight: '600',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem'
                        }}
                        title="Save directly to file (Chrome/Edge only)"
                    >
                        💾 Save to File
                    </button>
                    <button
                        onClick={handleDownloadJson}
                        style={{
                            padding: '0.5rem 1rem',
                            background: '#1DB954', // Green
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontWeight: '600'
                        }}
                        title="Download file to manually replace"
                    >
                        ⬇️ Download JSON
                    </button>
                    <button onClick={onExit} style={{ padding: '0.5rem 1rem', background: '#333', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                        Exit
                    </button>
                </div>
            </div>

            {/* Traffic Stats Section (NEW) */}
            <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', marginBottom: '2rem' }}>
                <h2 style={{ marginTop: 0, marginBottom: '1rem', color: '#333' }}>📊 Traffic Stats</h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                    <div style={{ padding: '1rem', background: '#f9f9f9', borderRadius: '8px', border: '1px solid #eee' }}>
                        <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Total Visits</div>
                        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1DB954' }}>
                            {visitCount !== null ? visitCount.toLocaleString() : 'Loading...'}
                        </div>
                    </div>
                    <div style={{ padding: '1rem', background: '#f9f9f9', borderRadius: '8px', border: '1px solid #eee' }}>
                        <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.5rem' }}>Your IP Address</div>
                        <div style={{ fontSize: '1.25rem', fontFamily: 'monospace', fontWeight: 'bold', color: '#333' }}>
                            {adminIp || 'Loading...'}
                        </div>
                    </div>
                </div>

                {/* Visitor Log (Latest 50) */}
                <div style={{ marginTop: '1.5rem' }}>
                    <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: '#555' }}>Recent Visitors (Log File)</h3>
                    <div style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #eee', borderRadius: '4px' }}>
                        <VisitorLogTable />
                    </div>
                </div>
            </div>

            {/* Support Settings Section */}
            <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', marginBottom: '2rem' }}>
                <h2 style={{ marginTop: 0, marginBottom: '1.5rem', color: '#333' }}>☕ Support Settings</h2>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Support Image (QR Code):</label>
                    <div style={{ marginBottom: '1rem' }}>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => {
                                const file = e.target.files?.[0];
                                if (file) {
                                    const reader = new FileReader();
                                    reader.onloadend = () => {
                                        const base64String = reader.result as string;
                                        localStorage.setItem('supportImage', base64String);
                                        alert('Image uploaded! Changes will appear after refreshing the page.');
                                    };
                                    reader.readAsDataURL(file);
                                }
                            }}
                            style={{
                                padding: '0.5rem',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '0.9rem',
                                width: '100%'
                            }}
                        />
                        <p style={{ fontSize: '0.85rem', color: '#666', marginTop: '0.5rem', marginBottom: 0 }}>
                            Upload a new QR code or support image (JPG, PNG, etc.)
                        </p>
                    </div>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Support Link URL:</label>
                    <input
                        type="text"
                        value={supportLink}
                        onChange={e => setSupportLink(e.target.value)}
                        placeholder="https://buymeacoffee.com/username"
                        style={{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ccc',
                            borderRadius: '4px',
                            fontSize: '1rem'
                        }}
                    />
                </div>

                <button
                    onClick={handleSaveSupportSettings}
                    style={{
                        padding: '0.75rem 1.5rem',
                        background: '#FFDD00',
                        color: '#000',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        fontSize: '1rem'
                    }}
                >
                    💾 Save Support Settings
                </button>
            </div>

            {/* Password Settings Section */}
            <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', marginBottom: '2rem' }}>
                <h2 style={{ marginTop: 0, marginBottom: '1.5rem', color: '#333' }}>🔒 Change Admin Password</h2>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>New Password:</label>
                    <input
                        type="password"
                        value={newPassword}
                        onChange={e => setNewPassword(e.target.value)}
                        placeholder="Enter new password (min 6 characters)"
                        style={{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ccc',
                            borderRadius: '4px',
                            fontSize: '1rem'
                        }}
                    />
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Confirm Password:</label>
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={e => setConfirmPassword(e.target.value)}
                        placeholder="Confirm new password"
                        style={{
                            width: '100%',
                            padding: '0.75rem',
                            border: '1px solid #ccc',
                            borderRadius: '4px',
                            fontSize: '1rem'
                        }}
                    />
                </div>

                <button
                    onClick={handleChangePassword}
                    style={{
                        padding: '0.75rem 1.5rem',
                        background: '#1DB954',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        fontSize: '1rem'
                    }}
                >
                    🔐 Change Password
                </button>
                <p style={{ fontSize: '0.85rem', color: '#666', marginTop: '1rem', marginBottom: 0 }}>
                    Default password: admin123 (if not changed)
                </p>
            </div>

            {editingId ? (
                <div className="edit-form" style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ marginTop: 0 }}>Editing Episode {editingId}</h3>
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Title:</label>
                        <input
                            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ccc', borderRadius: '4px' }}
                            value={editForm.title || ''}
                            onChange={e => setEditForm(prev => ({ ...prev, title: e.target.value }))}
                        />
                    </div>
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Description:</label>
                        <textarea
                            style={{ width: '100%', padding: '0.75rem', minHeight: '100px', border: '1px solid #ccc', borderRadius: '4px' }}
                            value={editForm.description || ''}
                            onChange={e => setEditForm(prev => ({ ...prev, description: e.target.value }))}
                        />
                    </div>
                    {/* Folder/Category */}
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Folder (Category):</label>
                        <input
                            style={{ width: '100%', padding: '0.75rem', border: '1px solid #ccc', borderRadius: '4px' }}
                            value={editForm.folder || ''}
                            onChange={e => setEditForm(prev => ({ ...prev, folder: e.target.value }))}
                        />
                    </div>

                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <button onClick={handleSave} style={{ padding: '0.75rem 1.5rem', background: '#1DB954', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: '600' }}>Save Changes</button>
                        <button onClick={() => setEditingId(null)} style={{ padding: '0.75rem 1.5rem', background: '#ccc', color: '#333', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Cancel</button>
                    </div>
                </div>
            ) : (
                <div className="episode-table" style={{ background: 'white', borderRadius: '8px', overflowX: 'auto', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                    <table style={{ width: '100%', minWidth: '600px', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: '#f5f5f5', textAlign: 'left' }}>
                                <th style={{ padding: '15px' }}>ID</th>
                                <th style={{ padding: '15px' }}>Title</th>
                                <th style={{ padding: '15px' }}>Category</th>
                                <th style={{ padding: '15px' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {episodes.map(ep => (
                                <tr key={ep.id} style={{ borderBottom: '1px solid #eee' }}>
                                    <td style={{ padding: '15px' }}>{ep.id}</td>
                                    <td style={{ padding: '15px', fontWeight: '500' }}>{ep.title}</td>
                                    <td style={{ padding: '15px' }}>
                                        <span style={{ background: '#eee', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.85rem' }}>
                                            {ep.folder}
                                        </span>
                                    </td>
                                    <td style={{ padding: '15px' }}>
                                        <button
                                            onClick={() => handleEdit(ep)}
                                            style={{
                                                cursor: 'pointer',
                                                background: '#f0f0f0',
                                                border: '1px solid #ddd',
                                                padding: '0.5rem',
                                                borderRadius: '4px'
                                            }}
                                            title="Edit"
                                        >
                                            ✏️
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};
