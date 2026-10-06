import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

def process_overlay(match):
    overlay = match.group(0)
    parts = re.split(r'<div class="detail-card">', overlay)
    
    if len(parts) >= 5:
        # text processing for length
        text1 = re.sub(r'<[^>]+>', '', parts[1]).strip()
        text2 = re.sub(r'<[^>]+>', '', parts[2]).strip()
        text3 = re.sub(r'<[^>]+>', '', parts[3]).strip()
        text4 = re.sub(r'<[^>]+>', '', parts[4].split('<div class="detail-card detail-card--wide')[0]).strip()
        
        l1 = len(text1) + parts[1].count('<li>') * 50
        l2 = len(text2) + parts[2].count('<li>') * 50
        l3 = len(text3) + parts[3].count('<li>') * 50
        l4 = len(text4) + parts[4].count('<li>') * 50
        
        t1 = l1 + l2
        t2 = l3 + l4
        
        pct1 = round(l1/t1*100)
        pct2 = 100 - pct1
        pct3 = round(l3/t2*100)
        pct4 = 100 - pct3
        
        # reconstruct the string with spans
        new_overlay = parts[0] + \
                      f'<div class="detail-card" style="grid-column: span {pct1};">' + parts[1] + \
                      f'<div class="detail-card" style="grid-column: span {pct2};">' + parts[2] + \
                      f'<div class="detail-card" style="grid-column: span {pct3};">' + parts[3] + \
                      f'<div class="detail-card" style="grid-column: span {pct4};">' + parts[4]
                      
        return new_overlay
    return overlay

# Apply to each overlay
html = re.sub(r'<article class="standard-detail-overlay".*?</article>', process_overlay, html, flags=re.DOTALL)

# Update CSS grid
html = html.replace('grid-template-columns: 11fr 9fr;', 'grid-template-columns: repeat(100, 1fr);')
html = html.replace('grid-column: span 2;', 'grid-column: span 100;')

# Update mobile media query
# We need to insert `.detail-bento > .detail-card { grid-column: span 100 !important; }`
# after `.detail-bento { grid-template-columns: 1fr; }`
media_query_addition = """
      .detail-bento > .detail-card {
        grid-column: span 100 !important;
      }
"""
html = html.replace('grid-template-columns: 1fr;\n      }\n      .detail-card--wide {',
                    'grid-template-columns: 1fr;\n      }\n' + media_query_addition + '      .detail-card--wide {')

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(html)

