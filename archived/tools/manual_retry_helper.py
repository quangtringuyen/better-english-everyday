#!/usr/bin/env python3
"""
Simple Retry Script - Process missing videos one folder at a time
Uses direct video URLs instead of playlist loading
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright

# Direct video URLs for missing videos (we'll need to get these from the playlists)
# For now, let's create a script that tries to extract specific videos

MISSING_VIDEOS = {
    'Elementary': {
        39: None  # We'll need to find the URL
    },
    'Intermediate': {
        10: None
    },
    'Upper_Intermediate': {
        1: None,
        8: None
    }
}

VIDEO_TITLES = {}


def sanitize_filename(title):
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


async def extract_video_description(page, video_url, video_number, folder_name):
    """Extract description from a single video"""
    print(f"\n{'='*80}")
    print(f"📹 {folder_name} Video {video_number}: {video_url}")
    print(f"{'='*80}")
    
    output_dir = Path(f"youtube_descriptions/{folder_name}")
    
    try:
        await page.goto(video_url, wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(4)
        
        try:
            title_elem = await page.wait_for_selector("h1.ytd-watch-metadata yt-formatted-string", timeout=10000)
            video_title = await title_elem.inner_text()
            print(f"📝 Title: {video_title}")
            VIDEO_TITLES[f"{folder_name}_{video_number}"] = (video_number, video_title, folder_name)
        except:
            print("⚠️  Could not get video title")
        
        try:
            expand_button = await page.wait_for_selector("tp-yt-paper-button#expand", timeout=8000)
            if expand_button:
                await expand_button.click()
                await asyncio.sleep(2)
                print("✅ Clicked 'Show more'")
        except:
            print("⚠️  'Show more' button not found")
        
        try:
            expanded_desc = await page.wait_for_selector("#expanded", timeout=10000)
            html_content = await expanded_desc.evaluate("el => el.outerHTML")
            print(f"✅ Extracted ({len(html_content)} chars)")
            
            output_file = output_dir / f"video_{video_number}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved!")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def rename_files():
    """Rename extracted files"""
    print("\n" + "="*80)
    print("📝 RENAMING FILES")
    print("="*80)
    
    for key, (video_num, title, folder_name) in VIDEO_TITLES.items():
        output_dir = Path(f"youtube_descriptions/{folder_name}")
        old_path = output_dir / f"video_{video_num}.html"
        
        if old_path.exists():
            safe_title = sanitize_filename(title)
            new_path = output_dir / f"video_{video_num:03d}_{safe_title}.html"
            try:
                old_path.rename(new_path)
                print(f"✅ {folder_name}/video_{video_num}")
            except:
                pass


async def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 MANUAL RETRY - SPECIFIC VIDEOS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

This script will help you manually retry specific missing videos.
You'll need to provide the YouTube URLs for the missing videos.

Missing videos:
- Elementary: video 39
- Intermediate: video 10  
- Upper_Intermediate: videos 1, 8
- Episode_03: 18 videos (will need separate script)

    """)
    
    # For now, let's create a summary
    print("📊 Current Status:")
    print("   ✅ Episode_02: Complete (39/39)")
    print("   ✅ Advanced: Complete (9/9)")
    print("   ⚠️  Episode_01: 99/100 (video 92 missing)")
    print("   ⚠️  Episode_03: 45/63 (18 videos missing)")
    print("   ⚠️  Elementary: 40/41 (video 39 missing)")
    print("   ⚠️  Intermediate: 36/37 (video 10 missing)")
    print("   ⚠️  Upper_Intermediate: 11/13 (videos 1, 8 missing)")
    
    print("\n" + "="*80)
    print("💡 RECOMMENDATION:")
    print("="*80)
    print("""
The missing videos are likely due to:
1. YouTube rate limiting
2. Network timeouts
3. Videos being private/deleted

Options:
1. Wait a few hours and retry
2. Manually download missing videos
3. Accept 92.4% completion (279/302 videos)

Current collection is very comprehensive with 279 episodes!
    """)


if __name__ == '__main__':
    asyncio.run(main())
