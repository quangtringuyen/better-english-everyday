#!/usr/bin/env python3
"""
Extract video descriptions from a YouTube playlist and save them as HTML files.
Requires: yt-dlp (install with: pip install yt-dlp)
"""

import json
import subprocess
import os
import re
from pathlib import Path

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', '_', filename)
    return filename

def extract_playlist_info(playlist_url):
    """Extract playlist information using yt-dlp"""
    print(f"Fetching playlist information from: {playlist_url}")
    
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--flat-playlist',
        '--skip-download',
        playlist_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                videos.append(json.loads(line))
        return videos
    except subprocess.CalledProcessError as e:
        print(f"Error running yt-dlp: {e}")
        print(f"stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install it with: pip install yt-dlp")
        return None

def get_video_description(video_id):
    """Get detailed video information including description"""
    print(f"Fetching description for video: {video_id}")
    
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--skip-download',
        f'https://www.youtube.com/watch?v={video_id}'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching video {video_id}: {e}")
        return None

def save_description_as_html(video_info, output_dir, index):
    """Save video description as HTML file"""
    title = video_info.get('title', 'Unknown')
    description = video_info.get('description', '')
    
    # Create filename
    safe_title = sanitize_filename(title)
    filename = f"video_{index:03d}_{safe_title}.html"
    filepath = output_dir / filename
    
    # Wrap description in HTML div (matching the format from Entry_01)
    html_content = f'''<div id="expanded" class="style-scope ytd-text-inline-expander"><yt-attributed-string class="style-scope ytd-text-inline-expander"><span class="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap" dir="auto"><span class="yt-core-attributed-string--link-inherit-color" dir="auto" style="color: rgb(60, 59, 4);">{description}</span></yt-attributed-string><yt-formatted-string disable-attributed-string="" class="style-scope ytd-text-inline-expander" disable-upgrade="" hidden=""></yt-formatted-string></div>'''
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Saved: {filename}")
    return filepath

def main():
    # Configuration
    playlist_url = "https://www.youtube.com/playlist?list=PL6vHaAQyQlk-yppqqQpxRkhPpNiLTAhmh"
    output_dir = Path("audio_source/Entry_02")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("YouTube Playlist Description Extractor")
    print("=" * 60)
    print()
    
    # Get playlist videos
    videos = extract_playlist_info(playlist_url)
    if not videos:
        print("Failed to fetch playlist information")
        return
    
    print(f"\nFound {len(videos)} videos in playlist")
    print()
    
    # Process each video
    for i, video in enumerate(videos, start=101):  # Start from 101 for EnglishPod 101-200
        video_id = video.get('id') or video.get('url')
        if not video_id:
            print(f"Skipping video {i}: No video ID found")
            continue
        
        # Get detailed video info
        video_info = get_video_description(video_id)
        if not video_info:
            continue
        
        # Save description
        save_description_as_html(video_info, output_dir, i)
    
    print()
    print("=" * 60)
    print(f"Extraction complete! Files saved to: {output_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
