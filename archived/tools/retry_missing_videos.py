#!/usr/bin/env python3
"""
Retry extraction for all missing videos across all playlists

This script will:
1. Identify missing videos in each folder
2. Re-extract only the missing ones
3. Auto-rename after extraction
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Playlist URLs
PLAYLISTS = {
    'Episode_03': {
        'url': 'https://www.youtube.com/playlist?list=PL6vHaAQyQlk8kP1SPJ9uvDcNA4Ujb6hue',
        'missing': [143, 146, 147, 150, 155, 168, 170, 173, 178, 179, 184, 187, 188, 190, 198, 199, 201, 202]
    },
    'Elementary': {
        'url': 'https://www.youtube.com/playlist?list=PL6vHaAQyQlk9L_lA9O4O-tRqT_zljx-lb',
        'missing': [39]
    },
    'Intermediate': {
        'url': 'https://www.youtube.com/playlist?list=PL6vHaAQyQlk9IInEy2bLpkaNlEt8JMCNB',
        'missing': [10]
    },
    'Upper_Intermediate': {
        'url': 'https://www.youtube.com/playlist?list=PL6vHaAQyQlk9XWaNN0HcA5-QnkvrSJi9w',
        'missing': [1, 8]
    }
}

VIDEO_TITLES = {}


def sanitize_filename(title):
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


async def get_playlist_videos(page, playlist_url):
    """Get all video URLs from the playlist"""
    print(f"📋 Loading playlist...")
    await page.goto(playlist_url, wait_until="networkidle", timeout=60000)
    await page.wait_for_selector("ytd-playlist-video-renderer", timeout=15000)
    
    print("📜 Scrolling to load all videos...")
    for i in range(20):
        await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        await asyncio.sleep(1.5)
    
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


async def extract_video_description(page, video_url, video_number, folder_name, retry_count=0):
    """Extract description from a single video with retry logic"""
    print(f"\n{'='*80}")
    print(f"📹 Processing {folder_name} Video {video_number}: {video_url}")
    if retry_count > 0:
        print(f"🔄 Retry attempt {retry_count}")
    print(f"{'='*80}")
    
    output_dir = Path(f"youtube_descriptions/{folder_name}")
    
    try:
        await page.goto(video_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(3)
        
        try:
            title_elem = await page.wait_for_selector("h1.ytd-watch-metadata yt-formatted-string", timeout=15000)
            video_title = await title_elem.inner_text()
            print(f"📝 Title: {video_title}")
            VIDEO_TITLES[f"{folder_name}_{video_number}"] = (video_number, video_title, folder_name)
        except:
            video_title = "Unknown"
            print("⚠️  Could not get video title")
        
        try:
            expand_button = await page.wait_for_selector("tp-yt-paper-button#expand, button#expand", timeout=10000)
            if expand_button:
                await expand_button.click()
                print("✅ Clicked 'Show more'")
                await asyncio.sleep(2)
        except:
            print("⚠️  'Show more' button not found")
        
        try:
            expanded_desc = await page.wait_for_selector("#expanded", timeout=15000)
            html_content = await expanded_desc.evaluate("el => el.outerHTML")
            print(f"✅ Extracted description HTML ({len(html_content)} characters)")
            
            output_file = output_dir / f"video_{video_number}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"💾 Saved to: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error extracting description: {e}")
            return False
            
    except PlaywrightTimeout as e:
        print(f"⏱️  Timeout error: {e}")
        
        if retry_count < 2:
            print(f"🔄 Retrying video {video_number}...")
            await asyncio.sleep(3)
            return await extract_video_description(page, video_url, video_number, folder_name, retry_count + 1)
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
    for key, (video_num, title, folder_name) in VIDEO_TITLES.items():
        output_dir = Path(f"youtube_descriptions/{folder_name}")
        old_filename = f"video_{video_num}.html"
        old_path = output_dir / old_filename
        
        if not old_path.exists():
            continue
        
        safe_title = sanitize_filename(title)
        new_filename = f"video_{video_num:03d}_{safe_title}.html"
        new_path = output_dir / new_filename
        
        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: {folder_name}/{old_filename} → {new_filename}")
            renamed += 1
        except Exception as e:
            print(f"❌ Error renaming {old_filename}: {e}")
    
    print(f"\n✅ Renamed {renamed} files")


async def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           RETRY MISSING VIDEOS - ALL PLAYLISTS                               ║
║           (Longer timeouts + retry logic)                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    total_missing = sum(len(p['missing']) for p in PLAYLISTS.values())
    print(f"📊 Total missing videos to retry: {total_missing}\n")
    
    async with async_playwright() as p:
        print("🚀 Launching browser...")
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        page.set_default_timeout(60000)
        
        try:
            total_successful = 0
            total_failed = 0
            
            for folder_name, playlist_info in PLAYLISTS.items():
                if not playlist_info['missing']:
                    continue
                
                print(f"\n{'='*80}")
                print(f"📁 Processing {folder_name}")
                print(f"{'='*80}")
                
                video_urls = await get_playlist_videos(page, playlist_info['url'])
                
                for missing_num in playlist_info['missing']:
                    if missing_num <= len(video_urls):
                        video_url = video_urls[missing_num - 1]
                        if await extract_video_description(page, video_url, missing_num, folder_name):
                            total_successful += 1
                        else:
                            total_failed += 1
                        
                        await asyncio.sleep(2)
            
            print("\n" + "="*80)
            print("📊 RETRY SUMMARY")
            print("="*80)
            print(f"✅ Successful: {total_successful} videos")
            print(f"❌ Failed: {total_failed} videos")
            print("="*80)
            
            if total_successful > 0:
                rename_files()
                print("\n🎉 COMPLETE!")
                print(f"✅ Recovered {total_successful} missing videos")
        
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
