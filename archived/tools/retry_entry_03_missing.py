#!/usr/bin/env python3
"""
Retry Missing Videos for Entry_03

This script extracts only the missing videos from Entry_03 playlist.
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Playlist URL for Entry_03
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL6vHaAQyQlk8kP1SPJ9uvDcNA4Ujb6hue"
OUTPUT_DIR = Path("audio_source/Entry_03")

# Missing video numbers
MISSING_VIDEOS = [202, 203, 205, 207, 209, 216, 233, 239, 242, 243, 247, 258, 259, 260, 262, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300]

# Store titles for renaming
VIDEO_TITLES = {}


def sanitize_filename(title):
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


async def get_playlist_videos(page):
    """Get all video URLs from the playlist"""
    print(f"📋 Loading playlist: {PLAYLIST_URL}")
    await page.goto(PLAYLIST_URL, wait_until="networkidle")
    
    await page.wait_for_selector("ytd-playlist-video-renderer", timeout=10000)
    
    print("📜 Scrolling to load all videos...")
    
    for i in range(20):
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
        await page.goto(video_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(2)
        
        # Get video title
        try:
            title_elem = await page.wait_for_selector("h1.ytd-watch-metadata yt-formatted-string", timeout=10000)
            video_title = await title_elem.inner_text()
            print(f"📝 Title: {video_title}")
            
            VIDEO_TITLES[video_number] = video_title
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
            
            # Save to file
            output_file = OUTPUT_DIR / f"video_{video_number}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error extracting description: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Error processing video: {e}")
        return False


def rename_files():
    """Rename all extracted files with their titles"""
    print("\n" + "="*80)
    print("📝 RENAMING FILES WITH TITLES")
    print("="*80 + "\n")
    
    renamed = 0
    
    for video_num, title in VIDEO_TITLES.items():
        old_filename = f"video_{video_num}.html"
        old_path = OUTPUT_DIR / old_filename
        
        if not old_path.exists():
            continue
        
        safe_title = sanitize_filename(title)
        new_filename = f"video_{video_num:03d}_{safe_title}.html"
        new_path = OUTPUT_DIR / new_filename
        
        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: {old_filename} → {new_filename}")
            renamed += 1
        except Exception as e:
            print(f"❌ Error renaming {old_filename}: {e}")
    
    print(f"\n✅ Renamed {renamed} files")


async def main():
    """Main function"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           RETRY MISSING VIDEOS - ENTRY_03                                    ║
║           Missing: {len(MISSING_VIDEOS)} videos                                           ║
║           Folder: audio_source/Entry_03                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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
            # Get all video URLs
            video_urls = await get_playlist_videos(page)
            
            if not video_urls:
                print("❌ No videos found in playlist!")
                return
            
            print(f"\n📊 Total videos in playlist: {len(video_urls)}")
            print(f"🎯 Videos to retry: {len(MISSING_VIDEOS)}\n")
            
            # Create mapping of video number to URL
            video_map = {}
            for i, url in enumerate(video_urls, 201):
                video_map[i] = url
            
            # Process only missing videos
            successful = 0
            failed = 0
            
            for video_num in MISSING_VIDEOS:
                if video_num in video_map:
                    if await extract_video_description(page, video_map[video_num], video_num):
                        successful += 1
                    else:
                        failed += 1
                    await asyncio.sleep(1)
                else:
                    print(f"⚠️  Video {video_num} not found in playlist")
                    failed += 1
            
            # Summary
            print("\n" + "="*80)
            print("📊 RETRY SUMMARY")
            print("="*80)
            print(f"✅ Successful: {successful} videos")
            print(f"❌ Failed: {failed} videos")
            print(f"📁 Files saved in: {OUTPUT_DIR.absolute()}")
            print("="*80)
            
            # Auto-rename files
            if successful > 0:
                rename_files()
                
                print("\n🎉 RETRY COMPLETE!")
                print(f"✅ Extracted {successful} missing videos")
                print(f"✅ Files renamed with titles")
                print(f"📁 Location: {OUTPUT_DIR.absolute()}")
        
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
