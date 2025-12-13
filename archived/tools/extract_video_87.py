#!/usr/bin/env python3
"""
Extract video 87 with retry logic and longer timeout
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

OUTPUT_DIR = Path("youtube_descriptions")
VIDEO_URL_87 = "https://www.youtube.com/watch?v=cdXjJyrd9vs"
VIDEO_NUM = 87


async def extract_video_87_with_retry(max_retries=3):
    """Extract video 87 with multiple retry attempts"""
    
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
        
        for attempt in range(1, max_retries + 1):
            print(f"\n{'='*80}")
            print(f"🎯 Attempt {attempt}/{max_retries} - Extracting Video 87")
            print(f"{'='*80}")
            
            try:
                print(f"📹 Navigating to: {VIDEO_URL_87}")
                await page.goto(VIDEO_URL_87, timeout=60000)  # 60 second timeout
                print("✅ Page loaded")
                
                await asyncio.sleep(5)  # Wait for page to fully load
                
                # Get video title
                try:
                    title_elem = await page.wait_for_selector("h1.ytd-watch-metadata yt-formatted-string", timeout=15000)
                    video_title = await title_elem.inner_text()
                    print(f"📝 Title: {video_title}")
                except Exception as e:
                    print(f"⚠️  Could not get video title: {e}")
                    video_title = "Unknown"
                
                # Click "Show more" button
                try:
                    print("🔍 Looking for 'Show more' button...")
                    expand_button = await page.wait_for_selector(
                        "tp-yt-paper-button#expand, button#expand",
                        timeout=10000
                    )
                    
                    if expand_button:
                        await expand_button.click()
                        print("✅ Clicked 'Show more'")
                        await asyncio.sleep(3)
                except Exception as e:
                    print(f"⚠️  Could not click 'Show more': {e}")
                
                # Extract the expanded description
                try:
                    print("📥 Extracting description...")
                    expanded_desc = await page.wait_for_selector("#expanded", timeout=15000)
                    html_content = await expanded_desc.evaluate("el => el.outerHTML")
                    print(f"✅ Extracted description HTML ({len(html_content)} characters)")
                    
                    # Save to file
                    output_file = OUTPUT_DIR / f"video_{VIDEO_NUM}.html"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    print(f"💾 Saved to: {output_file}")
                    print(f"\n🎉 SUCCESS! Video 87 extracted: {video_title}")
                    
                    await browser.close()
                    return True, video_title
                    
                except Exception as e:
                    print(f"❌ Error extracting description: {e}")
                    if attempt < max_retries:
                        print(f"⏳ Waiting 5 seconds before retry...")
                        await asyncio.sleep(5)
                    continue
            
            except Exception as e:
                print(f"❌ Error on attempt {attempt}: {e}")
                if attempt < max_retries:
                    print(f"⏳ Waiting 5 seconds before retry...")
                    await asyncio.sleep(5)
                continue
        
        print(f"\n❌ Failed to extract video 87 after {max_retries} attempts")
        await browser.close()
        return False, None


async def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           EXTRACT VIDEO 87 - WITH RETRY LOGIC                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    success, title = await extract_video_87_with_retry(max_retries=3)
    
    if success:
        print("\n" + "="*80)
        print("✅ EXTRACTION SUCCESSFUL!")
        print("="*80)
        print(f"Video 87: {title}")
        print("\n🎉 NEXT STEPS:")
        print("   1. Run: python3 manual_rename.py")
        print("   2. Run: python3 process_descriptions.py")
        print("   3. You'll have 99/100 episodes!")
    else:
        print("\n" + "="*80)
        print("❌ EXTRACTION FAILED")
        print("="*80)
        print("Video 87 could not be extracted.")
        print("This video might be:")
        print("  - Restricted in your region")
        print("  - Removed from YouTube")
        print("  - Having technical issues")


if __name__ == '__main__':
    asyncio.run(main())
