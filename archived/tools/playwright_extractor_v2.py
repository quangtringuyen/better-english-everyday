#!/usr/bin/env python3
"""
Automated YouTube Playlist Extractor using Playwright - Enhanced Version

Saves files with both number and title for easy identification.
Example: video_001_EnglishPod_1_Elementary_Difficult_Customer.html

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python3 playwright_extractor_v2.py
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Playlist URL
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi"
OUTPUT_DIR = Path("youtube_descriptions")


def sanitize_filename(title):
    """Convert title to safe filename"""
    # Remove special characters, keep alphanumeric, spaces, and hyphens
    safe = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe)
    # Remove multiple underscores
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


async def get_playlist_videos(page):
    """Get all video URLs from the playlist"""
    print(f"📋 Loading playlist: {PLAYLIST_URL}")
    await page.goto(PLAYLIST_URL, wait_until="networkidle")
    
    await page.wait_for_selector("ytd-playlist-video-renderer", timeout=10000)
    
    print("📜 Scrolling to load all videos...")
    
    for i in range(15):
        await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        await asyncio.sleep(1)
    
    video_elements = await page.query_selector_all("a#video-title")
    video_urls = []
    
    for elem in video_elements:
        url = await elem.get_attribute("href")
        if url and "/watch?v=" in url:
            video_id = url.split("/watch?v=")[1].split("&")[0]
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
            if clean_url not in video_urls:
                video_urls.append(clean_url)
    
    print(f"✅ Found {len(video_urls)} videos in playlist")
    return video_urls


async def extract_video_description(page, video_url, video_number):
    """Extract description from a single video"""
    print(f"\n{'='*80}")
    print(f"📹 Processing Video {video_number}: {video_url}")
    print(f"{'='*80}")
    
    try:
        await page.goto(video_url, wait_until="networkidle")
        await asyncio.sleep(2)
        
        # Get video title
        try:
            title_elem = await page.wait_for_selector("h1.ytd-watch-metadata yt-formatted-string", timeout=10000)
            video_title = await title_elem.inner_text()
            print(f"📝 Title: {video_title}")
        except:
            video_title = "Unknown"
            print("⚠️  Could not get video title")
        
        # Click "Show more" button
        try:
            expand_button = await page.wait_for_selector(
                "tp-yt-paper-button#expand, button#expand",
                timeout=5000
            )
            
            if expand_button:
                await expand_button.click()
                print("✅ Clicked 'Show more'")
                await asyncio.sleep(1.5)
        except PlaywrightTimeout:
            print("⚠️  'Show more' button not found, description might already be expanded")
        except Exception as e:
            print(f"⚠️  Could not click 'Show more': {e}")
        
        # Extract the expanded description
        try:
            expanded_desc = await page.wait_for_selector("#expanded", timeout=10000)
            html_content = await expanded_desc.evaluate("el => el.outerHTML")
            print(f"✅ Extracted description HTML ({len(html_content)} characters)")
            
            # Create filename with number and title
            safe_title = sanitize_filename(video_title)
            filename = f"video_{video_number:03d}_{safe_title}.html"
            output_file = OUTPUT_DIR / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {output_file.name}")
            return True
            
        except Exception as e:
            print(f"❌ Error extracting description: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Error processing video: {e}")
        return False


async def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           YOUTUBE ENGLISHPOD EXTRACTOR V2                                    ║
║           (Saves with video titles in filename)                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}\n")
    
    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        try:
            video_urls = await get_playlist_videos(page)
            
            if not video_urls:
                print("❌ No videos found in playlist!")
                return
            
            print(f"\n📊 Total videos found: {len(video_urls)}")
            num_videos = len(video_urls)
            
            print(f"\n🎬 Processing {num_videos} videos...\n")
            
            successful = 0
            failed = 0
            
            for i, video_url in enumerate(video_urls[:num_videos], 1):
                if await extract_video_description(page, video_url, i):
                    successful += 1
                else:
                    failed += 1
                
                if i < num_videos:
                    await asyncio.sleep(1)
            
            print("\n" + "="*80)
            print("📊 EXTRACTION SUMMARY")
            print("="*80)
            print(f"✅ Successful: {successful} videos")
            print(f"❌ Failed: {failed} videos")
            print(f"📁 Files saved in: {OUTPUT_DIR.absolute()}")
            print("="*80)
            
            if successful > 0:
                print("\n🎉 NEXT STEP:")
                print("   Run: python3 process_descriptions.py")
                print("   This will generate the TypeScript file with all episodes!")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Extraction interrupted by user")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            print("\n🔒 Closing browser...")
            await browser.close()
            print("✅ Done!")


if __name__ == '__main__':
    asyncio.run(main())
