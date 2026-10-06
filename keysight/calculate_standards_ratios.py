import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

def process_overlay(match):
    overlay_content = match.group(0)
    
    # We will find the 4 detail-card divs (not the wide one, which has detail-card--wide)
    # The regex below matches <div class="detail-card"> but NOT if it has detail-card--wide
    # Wait, the class attribute might have other things, let's capture the whole tag
    # Actually, we can use re.split to carefully process each card.
    
    cards = re.split(r'(<div class="detail-card">)', overlay_content)
    
    if len(cards) < 9: # Needs at least 4 split points (9 pieces)
        return overlay_content
        
    # cards[0] is before first card
    # cards[1] is '<div class="detail-card">'
    # cards[2] is content of card 1 (up to next div)
    # Actually, regex split with capturing groups can be messy if there are nested divs.
    
    return overlay_content

# We can use a simpler approach. We know the exact structure:
# <div class="detail-card">
#   <div class="detail-card__header">...</div>
#   <div class="detail-card__content">...</div>
# </div>
# Repeated 4 times, then the wide card.

