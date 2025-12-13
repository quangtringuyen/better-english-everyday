#!/usr/bin/env python3
"""
Extract specific missing videos from YouTube playlist

This script extracts only the missing episodes: 54, 87, 92
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Playlist URL
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi"
OUTPUT_DIR = Path("youtube_descriptions")

# Missing video numbers
MISSING_VIDEOS = [54, 87, 92]


async def extract_specific_video(page, video_url, video_number):
    """Extract description from a specific video"""
    print(f"\n{'='*80}")
    print(f"📹 Extracting Video {video_number}: {video_url}")
    print(f"{'='*80}")
    
    try:
        await page.goto(video_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        
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
                await asyncio.sleep(2)
        except PlaywrightTimeout:
            print("⚠️  'Show more' button not found, trying to continue anyway...")
        except Exception as e:
            print(f"⚠️  Could not click 'Show more': {e}")
        
        # Extract the expanded description
        try:
            expanded_desc = await page.wait_for_selector("#expanded", timeout=10000)
            html_content = await expanded_desc.evaluate("el => el.outerHTML")
            print(f"✅ Extracted description HTML ({len(html_content)} characters)")
            
            # Save to file
            output_file = OUTPUT_DIR / f"video_{video_number}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {output_file}")
            return True, video_title
            
        except Exception as e:
            print(f"❌ Error extracting description: {e}")
            return False, None
    
    except Exception as e:
        print(f"❌ Error processing video: {e}")
        return False, None


async def get_video_url_by_index(page, index):
    """Get video URL from playlist by index"""
    print(f"📋 Loading playlist to find video {index}...")
    await page.goto(PLAYLIST_URL, wait_until="networkidle")
    
    await page.wait_for_selector("ytd-playlist-video-renderer", timeout=10000)
    
    # Scroll to load all videos
    print("📜 Scrolling to load videos...")
    for i in range(15):
        await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        await asyncio.sleep(1)
    
    # Get all video links
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
    
    if index <= len(video_urls):
        return video_urls[index - 1]
    else:
        print(f"❌ Video {index} not found in playlist (only {len(video_urls)} videos available)")
        return None


async def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           EXTRACT MISSING VIDEOS                                             ║
║           Videos: 54, 87, 92                                                 ║
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
        
        results = {}
        
        try:
            for video_num in MISSING_VIDEOS:
                print(f"\n{'='*80}")
                print(f"🎯 Processing Missing Video {video_num}")
                print(f"{'='*80}")
                
                # Get video URL from playlist
                video_url = await get_video_url_by_index(page, video_num)
                
                if video_url:
                    success, title = await extract_specific_video(page, video_url, video_num)
                    results[video_num] = {
                        'success': success,
                        'title': title,
                        'url': video_url
                    }
                else:
                    results[video_num] = {
                        'success': False,
                        'title': None,
                        'url': None
                    }
                
                await asyncio.sleep(2)
            
            # Summary
            print("\n" + "="*80)
            print("📊 EXTRACTION SUMMARY")
            print("="*80)
            
            successful = sum(1 for r in results.values() if r['success'])
            failed = len(results) - successful
            
            print(f"✅ Successful: {successful} videos")
            print(f"❌ Failed: {failed} videos")
            print("\nDetails:")
            
            for video_num, result in results.items():
                if result['success']:
                    print(f"  ✅ Video {video_num}: {result['title']}")
                else:
                    print(f"  ❌ Video {video_num}: Failed to extract")
            
            print("="*80)
            
            if successful > 0:
                print("\n🎉 NEXT STEPS:")
                print("   1. Run: python3 manual_rename.py (to rename new files)")
                print("   2. Run: python3 process_descriptions.py (to regenerate TypeScript)")
                print("   3. Refresh your app to see the new episodes!")
        
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
