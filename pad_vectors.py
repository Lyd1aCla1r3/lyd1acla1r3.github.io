import re
import glob

def process_file(filepath):
    with open(filepath, 'r') as f:
        text = f.read()
        
    original = text

    def process_math(match):
        chunk = match.group(0)
        chunk = re.sub(r'(?<![-\}\d.])(\d+\.\d+)', r'\\phantom{-}\1', chunk)
        chunk = chunk.replace(r'\mathbf{\phantom{-}', r'\phantom{-}\mathbf{')
        # Also handle \mathbf{ \phantom{-} -> \phantom{-}\mathbf{ if there's a space? Just in case.
        return chunk
    
    text = re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}', process_math, text, flags=re.DOTALL)
    
    def process_table_row(match):
        chunk = match.group(0)
        # We only want to pad numbers inside vectors like [...] 
        # But some rows have [...] and others have just numbers.
        # It's safer to just pad all positive decimals in the row if the row is a math row.
        # But wait, what if the decimal is part of an angle? Like 57.3?
        # The user said "add padding after the last digit of each vector in the summary tables" and "execute that same vector padding throughout the blog series".
        if '[' in chunk and ']' in chunk:
            chunk = re.sub(r'(?<![-\}\d.])(\d+\.\d+)', r'\\phantom{-}\1', chunk)
            chunk = chunk.replace(r'\mathbf{\phantom{-}', r'\phantom{-}\mathbf{')
        return chunk
        
    text = re.sub(r'^\|.*\|$', process_table_row, text, flags=re.MULTILINE)
    
    if text != original:
        with open(filepath, 'w') as f:
            f.write(text)
        print(f"Updated {filepath}")

files = glob.glob('/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/*.md')
for f in files:
    process_file(f)

