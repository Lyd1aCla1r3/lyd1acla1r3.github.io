import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'r', encoding='utf-8') as f:
    html = f.read()

def process_overlay(match):
    overlay_content = match.group(0)
    
    # Find all cards in this overlay
    cards = re.findall(r'<div class="detail-card">(.*?)</div>\s*(?=<div class="detail-card"|<div class="detail-card detail-card--wide|</article)', overlay_content, re.DOTALL)
    
    if len(cards) >= 2:
        # Strip html tags to count chars
        text1 = re.sub(r'<[^>]+>', '', cards[0])
        text2 = re.sub(r'<[^>]+>', '', cards[1])
        
        # approximate visual weight (chars)
        len1 = len(text1.strip())
        len2 = len(text2.strip())
        
        if len1 + len2 > 0:
            total = len1 + len2
            pct1 = round((len1 / total) * 100)
            pct2 = 100 - pct1
            
            print(f"Computed ratio {pct1}fr {pct2}fr")
            
            # replace the FIRST <div class="detail-bento"> in this overlay with the styled one
            # handle cases where it might already have a style
            overlay_content = re.sub(r'<div class="detail-bento"(?: style="[^"]*")?>', f'<div class="detail-bento" style="grid-template-columns: {pct1}fr {pct2}fr;">', overlay_content, count=1)
            
    return overlay_content

# We need to process each <article class="standard-detail-overlay"...>...</article> individually
# But re.sub with a function is perfect for this.
new_html = re.sub(r'<article class="standard-detail-overlay".*?</article>', process_overlay, html, flags=re.DOTALL)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
