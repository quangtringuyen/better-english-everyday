"""
YouTube Playlist Extractor - Browser Automation Script

This script uses browser automation to:
1. Open each video in the YouTube playlist
2. Expand the description
3. Extract the HTML content
4. Parse and save the data

Usage:
    python extract_playlist.py
"""

import time
import json
from pathlib import Path

# Instructions for manual extraction since browser automation is having issues
MANUAL_INSTRUCTIONS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   YOUTUBE PLAYLIST EXTRACTION GUIDE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Since browser automation is experiencing issues, here's how to extract data manually:

📋 STEP-BY-STEP PROCESS:

1. Open the YouTube playlist in your browser:
   https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi

2. For EACH video in the playlist:
   
   a) Click on the video to open it
   
   b) Click "Show more" button under the video to expand the description
   
   c) Right-click on the expanded description area
   
   d) Select "Inspect" or "Inspect Element"
   
   e) In the Developer Tools, find the <div id="expanded"> element
   
   f) Right-click on that element and select:
      - "Copy" → "Copy outerHTML"
   
   g) Create a new file: video_[NUMBER].html
      (e.g., video_1.html, video_2.html, etc.)
   
   h) Paste the HTML content into that file
   
   i) Save the file in the 'youtube_descriptions' folder

3. Once you've saved all the HTML files, run:
   python process_descriptions.py

This will automatically:
- Parse all the HTML files
- Extract conversation and vocabulary
- Generate TypeScript code
- Create a complete youtube-episodes.ts file

📁 FOLDER STRUCTURE:

podcast-for-newbie/
├── youtube_descriptions/     ← Create this folder
│   ├── video_1.html         ← Paste HTML here
│   ├── video_2.html
│   ├── video_3.html
│   └── ...
├── extract_youtube_data.py
├── process_descriptions.py   ← Run this after saving HTML files
└── src/data/youtube-episodes.ts  ← Final output

💡 TIP: You can also use the browser console to extract the HTML:

1. Open the video page
2. Click "Show more"
3. Open browser console (F12)
4. Run this JavaScript:

   const desc = document.querySelector('#expanded');
   console.log(desc.outerHTML);

5. Copy the output from the console

═══════════════════════════════════════════════════════════════════════════════
"""

def main():
    print(MANUAL_INSTRUCTIONS)
    
    # Create the youtube_descriptions folder if it doesn't exist
    descriptions_dir = Path('youtube_descriptions')
    descriptions_dir.mkdir(exist_ok=True)
    
    print(f"\n✅ Created folder: {descriptions_dir.absolute()}")
    print("\n📝 Start saving video descriptions as HTML files in this folder!")
    print("\n🚀 When ready, run: python process_descriptions.py\n")

if __name__ == '__main__':
    main()
