// ============================================================================
// YOUTUBE ENGLISHPOD EXTRACTOR - BROWSER CONSOLE SCRIPT
// ============================================================================
// 
// HOW TO USE:
// 1. Open a video from the EnglishPod playlist
// 2. Click "Show more" to expand the description
// 3. Press F12 to open Developer Tools
// 4. Go to the Console tab
// 5. Copy and paste this ENTIRE script
// 6. Press Enter
// 7. Copy the HTML output and save as video_X.html
//
// ============================================================================

(function () {
    console.clear();
    console.log('%c========================================', 'color: #667eea; font-weight: bold; font-size: 16px');
    console.log('%c   YouTube EnglishPod Extractor', 'color: #667eea; font-weight: bold; font-size: 20px');
    console.log('%c========================================', 'color: #667eea; font-weight: bold; font-size: 16px');
    console.log('');

    // Get the expanded description
    const desc = document.querySelector('#expanded');

    if (!desc) {
        console.error('%c❌ ERROR: Description not found!', 'color: red; font-weight: bold; font-size: 16px');
        console.log('%cPlease click the "Show more" button first!', 'color: orange; font-size: 14px');
        return;
    }

    // Get video information
    const videoTitle = document.querySelector('h1.ytd-watch-metadata yt-formatted-string')?.textContent || 'Unknown';
    const videoId = new URLSearchParams(window.location.search).get('v') || 'unknown';
    const html = desc.outerHTML;

    // Display information
    console.log('%c✅ Extraction Successful!', 'color: green; font-weight: bold; font-size: 16px');
    console.log('');
    console.log('%cVideo Title:', 'color: #667eea; font-weight: bold');
    console.log(videoTitle);
    console.log('');
    console.log('%cVideo ID:', 'color: #667eea; font-weight: bold');
    console.log(videoId);
    console.log('');
    console.log('%c========================================', 'color: #667eea; font-weight: bold');
    console.log('%c   HTML OUTPUT (Copy everything below)', 'color: #667eea; font-weight: bold; font-size: 14px');
    console.log('%c========================================', 'color: #667eea; font-weight: bold');
    console.log('');
    console.log(html);
    console.log('');
    console.log('%c========================================', 'color: #667eea; font-weight: bold');
    console.log('');
    console.log('%c📝 NEXT STEPS:', 'color: #28a745; font-weight: bold; font-size: 14px');
    console.log('%c1. Copy the HTML above (between the lines)', 'color: #333');
    console.log('%c2. Create a file: youtube_descriptions/video_X.html', 'color: #333');
    console.log('%c3. Paste the HTML and save', 'color: #333');
    console.log('%c4. Repeat for other videos', 'color: #333');
    console.log('%c5. Run: python3 process_descriptions.py', 'color: #333');
    console.log('');

    // Try to copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(html).then(() => {
            console.log('%c✅ HTML copied to clipboard!', 'color: green; font-weight: bold; font-size: 14px');
            console.log('%cYou can now paste it directly into a file!', 'color: green');
        }).catch(() => {
            console.log('%c⚠️ Could not auto-copy. Please copy manually from above.', 'color: orange');
        });
    }

    // Create a download link
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const filename = `video_${videoId}.html`;

    console.log('');
    console.log('%c💾 Quick Download:', 'color: #667eea; font-weight: bold');
    console.log(`%cRun this to download: downloadFile('${filename}')`, 'color: #333; background: #f0f0f0; padding: 5px');

    // Make download function available globally
    window.downloadFile = function (name) {
        const a = document.createElement('a');
        a.href = url;
        a.download = name || filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        console.log('%c✅ File downloaded!', 'color: green; font-weight: bold');
    };

    console.log('');
    console.log('%c========================================', 'color: #667eea; font-weight: bold');
    console.log('');

})();

// ============================================================================
// QUICK COMMANDS:
// ============================================================================
// downloadFile()           - Download the HTML file
// downloadFile('video_2.html')  - Download with custom name
// ============================================================================
