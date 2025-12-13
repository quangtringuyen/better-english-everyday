#!/usr/bin/env python3
"""
Retry Episode_03 Missing Videos

Missing: [143, 146, 147, 150, 155, 168, 170, 173, 178, 179, 184, 187, 188, 190, 198, 199, 201, 202]
Total: 18 videos
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL6vHaAQyQlk8kP1SPJ9uvDcNA4Ujb6hue"
OUTPUT_DIR = Path("youtube_descriptions/Episode_03")
MISSING_VIDEOS = [143, 146, 147, 150, 155, 168, 170, 173, 178, 179, 184, 187, 188, 190, 198, 199, 201, 202]
VIDEO_TITLES = {}


def sanitize_filename(title):
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


async def get_playlist_videos(page):
    """Get all video URLs from the playlist"""
    print(f"📋 Loading Episode_03 playlist...")
    
    try:
        await page.goto(PLAYLIST_URL, wait_until="domcontentloaded", timeout=90000)
        await asyncio.sleep(3)
        
        await page.wait_for_selector("ytd-playlist-video-renderer", timeout=20000)
        
        print("📜 Scrolling to load all videos...")
        for i in range(25):
            await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            await asyncio.sleep(1.5)
        
        await asyncio.sleep(2)
        
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
        
    except Exception as e:
        print(f"❌ Error loading playlist: {e}")
        return []


async def extract_video_description(page, video_url, video_number, retry_count=0):
    """Extract description from a single video with retry logic"""
    print(f"\n{'='*80}")
    print(f"📹 Episode_03 Video {video_number}: {video_url}")
    if retry_count > 0:
        print(f"🔄 Retry attempt {retry_count}")
    print(f"{'='*80}")
    
    try:
        await page.goto(video_url, wait_until="domcontentloaded", timeout=90000)
        await asyncio.sleep(4)
        
        try:
            title_elem = await page.wait_for_selector("h1.ytd-watch-metadata yt-formatted-string", timeout=15000)
            video_title = await title_elem.inner_text()
            print(f"📝 Title: {video_title}")
            VIDEO_TITLES[video_number] = video_title
        except:
            video_title = "Unknown"
            print("⚠️  Could not get video title")
        
        try:
            expand_button = await page.wait_for_selector("tp-yt-paper-button#expand, button#expand", timeout=10000)
            if expand_button:
                await expand_button.click()
                print("✅ Clicked 'Show more'")
                await asyncio.sleep(2.5)
        except:
            print("⚠️  'Show more' button not found")
        
        try:
            expanded_desc = await page.wait_for_selector("#expanded", timeout=15000)
            html_content = await expanded_desc.evaluate("el => el.outerHTML")
            print(f"✅ Extracted description HTML ({len(html_content)} characters)")
            
            output_file = OUTPUT_DIR / f"video_{video_number}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error extracting description: {e}")
            return False
            
    except PlaywrightTimeout as e:
        print(f"⏱️  Timeout error")
        
        if retry_count < 2:
            print(f"🔄 Retrying video {video_number}...")
            await asyncio.sleep(5)
            return await extract_video_description(page, video_url, video_number, retry_count + 1)
        else:
            print(f"❌ Failed after {retry_count + 1} attempts")
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
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           EPISODE_03 RETRY - 18 MISSING VIDEOS                               ║
║           (Extended timeouts + retry logic)                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"📊 Missing videos to retry: {len(MISSING_VIDEOS)}")
    print(f"📋 Video numbers: {MISSING_VIDEOS}\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        page.set_default_timeout(90000)
        
        try:
            video_urls = await get_playlist_videos(page)
            
            if not video_urls:
                print("❌ Could not load playlist!")
                return
            
            if len(video_urls) < max(MISSING_VIDEOS):
                print(f"⚠️  Warning: Only found {len(video_urls)} videos, need at least {max(MISSING_VIDEOS)}")
            
            successful = 0
            failed = 0
            
            for missing_num in MISSING_VIDEOS:
                # Video numbers start at 140, so adjust index
                index = missing_num - 140
                
                if index < len(video_urls):
                    video_url = video_urls[index]
                    if await extract_video_description(page, video_url, missing_num):
                        successful += 1
                    else:
                        failed += 1
                    
                    # Longer delay between videos to avoid rate limiting
                    await asyncio.sleep(3)
                else:
                    print(f"⚠️  Video {missing_num} not found in playlist")
                    failed += 1
            
            print("\n" + "="*80)
            print("📊 RETRY SUMMARY - EPISODE_03")
            print("="*80)
            print(f"✅ Successful: {successful} videos")
            print(f"❌ Failed: {failed} videos")
            print(f"📁 Files saved in: {OUTPUT_DIR.absolute()}")
            print("="*80)
            
            if successful > 0:
                rename_files()
                print("\n🎉 COMPLETE!")
                print(f"✅ Recovered {successful} Episode_03 videos")
                print(f"📁 Location: {OUTPUT_DIR.absolute()}")
                
                # Show new total
                all_files = list(OUTPUT_DIR.glob("video_*.html"))
                print(f"\n📊 Episode_03 now has: {len(all_files)}/63 videos")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Retry interrupted by user")
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
