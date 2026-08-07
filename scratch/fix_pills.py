import os
import re

dir_path = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/tokenization'

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to find <b><code>...</code></b>
    # We want to replace it with <code>...</code> IF the inner content is:
    # 1. A single character (like 'w', 'a', 'k')
    # 2. '&lt;/w&gt;' or '</w>'
    
    def replacer(match):
        inner = match.group(1)
        # Check if single char (excluding HTML entities like &gt;, but here they are just 1 char if parsed, 
        # but in text it's a single character or a specific string)
        if len(inner) == 1 or inner == '&lt;/w&gt;' or inner == '</w>':
            return f'<code>{inner}</code>'
        return match.group(0) # Keep as is

    new_content = re.sub(r'<b><code>(.*?)</code></b>', replacer, content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")

for filename in os.listdir(dir_path):
    if filename.endswith('.md'):
        process_file(os.path.join(dir_path, filename))
