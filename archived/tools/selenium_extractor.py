#!/usr/bin/env python3
"""
Automated YouTube Playlist Extractor using Selenium

This script automatically:
1. Opens each video in the playlist
2. Clicks "Show more" to expand description
3. Extracts the HTML content
4. Saves to youtube_descriptions folder
5. Processes all videos automatically

Requirements:
    pip install selenium webdriver-manager

Usage:
    python3 selenium_extractor.py
"""

import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Playlist URL
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL6vHaAQyQlk9RH8F_1lsI_z9wn3SLZHDi"
OUTPUT_DIR = Path("youtube_descriptions")


def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    # Remove headless mode so you can see what's happening
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Automatically download and setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_playlist_videos(driver, playlist_url):
    """Get all video URLs from the playlist"""
    print(f"📋 Loading playlist: {playlist_url}")
    driver.get(playlist_url)
    
    # Wait for playlist to load
    time.sleep(3)
    
    # Scroll to load all videos
    print("📜 Scrolling to load all videos...")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    for _ in range(10):  # Scroll multiple times to load all videos
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Get all video links
    video_elements = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
    video_urls = []
    
    for elem in video_elements:
        url = elem.get_attribute("href")
        if url and "/watch?v=" in url:
            # Clean URL (remove playlist parameter)
            video_id = url.split("/watch?v=")[1].split("&")[0]
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
            if clean_url not in video_urls:
                video_urls.append(clean_url)
    
    print(f"✅ Found {len(video_urls)} videos in playlist")
    return video_urls


def extract_video_description(driver, video_url, video_number):
    """Extract description from a single video"""
    print(f"\n{'='*80}")
    print(f"📹 Processing Video {video_number}: {video_url}")
    print(f"{'='*80}")
    
    try:
        # Open video
        driver.get(video_url)
        time.sleep(3)
        
        # Get video title
        try:
            title_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ytd-watch-metadata yt-formatted-string"))
            )
            video_title = title_elem.text
            print(f"📝 Title: {video_title}")
        except:
            video_title = "Unknown"
            print("⚠️  Could not get video title")
        
        # Click "Show more" button
        try:
            # Try different selectors for the "Show more" button
            show_more_selectors = [
                "tp-yt-paper-button#expand",
                "button#expand",
                "#expand",
                "ytd-text-inline-expander tp-yt-paper-button"
            ]
            
            show_more_button = None
            for selector in show_more_selectors:
                try:
                    show_more_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if show_more_button:
                driver.execute_script("arguments[0].click();", show_more_button)
                print("✅ Clicked 'Show more'")
                time.sleep(2)
            else:
                print("⚠️  'Show more' button not found, description might already be expanded")
        
        except Exception as e:
            print(f"⚠️  Could not click 'Show more': {e}")
        
        # Extract the expanded description
        try:
            expanded_desc = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#expanded"))
            )
            html_content = expanded_desc.get_attribute("outerHTML")
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


def main():
    """Main function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AUTOMATED YOUTUBE ENGLISHPOD EXTRACTOR                             ║
║                     Using Selenium WebDriver                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}\n")
    
    # Setup driver
    print("🚀 Setting up Chrome WebDriver...")
    try:
        driver = setup_driver()
        print("✅ WebDriver ready!\n")
    except Exception as e:
        print(f"❌ Error setting up WebDriver: {e}")
        print("\n💡 Please install required packages:")
        print("   pip install selenium webdriver-manager")
        return
    
    try:
        # Get all video URLs
        video_urls = get_playlist_videos(driver, PLAYLIST_URL)
        
        if not video_urls:
            print("❌ No videos found in playlist!")
            return
        
        # Ask user how many videos to process
        print(f"\n📊 Total videos found: {len(video_urls)}")
        user_input = input(f"How many videos do you want to extract? (1-{len(video_urls)}, or 'all'): ").strip()
        
        if user_input.lower() == 'all':
            num_videos = len(video_urls)
        else:
            try:
                num_videos = int(user_input)
                num_videos = min(num_videos, len(video_urls))
            except:
                num_videos = 10
                print(f"⚠️  Invalid input, defaulting to {num_videos} videos")
        
        print(f"\n🎬 Processing {num_videos} videos...\n")
        
        # Process each video
        successful = 0
        failed = 0
        
        for i, video_url in enumerate(video_urls[:num_videos], 1):
            if extract_video_description(driver, video_url, i):
                successful += 1
            else:
                failed += 1
            
            # Small delay between videos
            if i < num_videos:
                time.sleep(2)
        
        # Summary
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
    
    finally:
        print("\n🔒 Closing browser...")
        driver.quit()
        print("✅ Done!")


if __name__ == '__main__':
    main()
