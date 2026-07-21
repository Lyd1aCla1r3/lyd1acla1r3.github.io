import json
import os
import time
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

def setup_directories():
    base_dir = Path(__file__).parent
    verified_dir = base_dir / "verified"
    verified_dir.mkdir(parents=True, exist_ok=True)
    return verified_dir

def capture_query(page, query, verified_dir):
    print(f"Capturing query: '{query}'")
    
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us"
    
    page.goto(url)
    
    # Wait a bit for JS to execute and potential AI Overview to render
    time.sleep(3)
    
    # AI Overviews are notoriously hard to select due to obfuscated classes.
    # We look for common markers like "AI Overview" text or specific container attributes.
    # If the exact selector fails in the future, update it here.
    ai_overview_selector = 'div[data-attrid="wa:/description"]' # Common for AI overviews, though fragile
    fallback_selector = 'text="AI Overview"'
    
    has_ai_overview = False
    overview_element = None
    
    fallback_used = False
    try:
        # Check if the block exists
        overview_element = page.locator(ai_overview_selector).first
        if not overview_element.is_visible():
             # Try fallback: find the text
             fallback = page.locator(fallback_selector).first
             if fallback.is_visible():
                 has_ai_overview = True
                 fallback_used = True
             
        if overview_element and overview_element.is_visible():
            has_ai_overview = True
    except TimeoutError:
        has_ai_overview = False

    if not has_ai_overview:
        print(f"  -> No AI Overview detected for '{query}'. Skipping.")
        return False
        
    print(f"  -> AI Overview detected! Capturing...")
    
    # Expand if there's a "Show more" button
    try:
        show_more = page.locator('text="Show more"').first
        if show_more.is_visible():
            show_more.click()
            time.sleep(1)
    except Exception:
        pass # No show more button
        
    # Get the bounding box of the whole results area or just the overview
    # Sometimes it's better to capture the top part of the page
    safe_filename = "".join([c if c.isalnum() else "_" for c in query])
    screenshot_path = verified_dir / f"{safe_filename}.png"
    
    # Screenshot the full page to avoid truncating expanded AI Overviews
    page.screenshot(path=str(screenshot_path), full_page=True)
    
    # Extract raw text and HTML for manual verification
    if fallback_used:
        # Use JS to traverse up to a div that represents the card, avoiding organic results
        fallback = page.locator(fallback_selector).first
        handle = fallback.element_handle()
        result = page.evaluate('''
            (el) => {
                let current = el;
                for(let i=0; i<8; i++) {
                    if(current.parentElement) {
                        current = current.parentElement;
                        if(current.id === "search" || current.id === "rcnt") {
                            let target = current.children[0] ? current.children[0] : current;
                            return {html: target.innerHTML, text: target.innerText};
                        }
                    }
                }
                return {html: current.innerHTML, text: current.innerText};
            }
        ''', handle)
        html_content = result['html']
        text_content = result['text']
    else:
        html_content = overview_element.inner_html() if overview_element else ""
        text_content = overview_element.inner_text() if overview_element else ""
    
    data = {
        "query": query,
        "has_ai_overview": True,
        "raw_text": text_content,
        "raw_html": html_content
    }
    
    json_path = verified_dir / f"{safe_filename}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"  -> Saved to {safe_filename}.png and {safe_filename}.json")
    return True

def main():
    verified_dir = setup_directories()
    
    # Load queries
    root_dir = Path(__file__).parent.parent
    queries_file = root_dir / "queries.json"
    
    with open(queries_file, 'r', encoding='utf-8') as f:
        queries = json.load(f)
        
    with sync_playwright() as p:
        user_data_dir = str(Path(__file__).parent / "browser_profile")
        
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            # Use a Mac user agent since you are on a Mac
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 1024},
            # This flag hides the "navigator.webdriver" property that Google uses to detect bots
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # In a persistent context, there is usually already a default page
        page = context.pages[0] if context.pages else context.new_page()
        
        # Optional: do a manual search first to solve any initial captchas
        page.goto("https://www.google.com")
        print("Please solve any captchas on the opened browser window within the next 20 seconds...")
        time.sleep(20)
        
        successful_captures = 0
        
        for item in queries:
            query = item["query"]
            success = capture_query(page, query, verified_dir)
            if success:
                successful_captures += 1
            
            # Be polite to Google
            time.sleep(4)
            
        print(f"\nCapture complete. Successfully captured {successful_captures} out of {len(queries)} queries.")
        context.close()

if __name__ == "__main__":
    main()
