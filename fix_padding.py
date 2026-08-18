import re
import glob

def clean_and_pad(filepath):
    with open(filepath, 'r') as f:
        text = f.read()

    # 1. Strip ALL \phantom{-} from the file to start fresh
    text = text.replace(r'\phantom{-}', '')
    text = text.replace(r'\;', '') # Strip the \; we added to tables too, we'll re-add carefully

    # 2. Pad table rows
    def process_table_row(match):
        chunk = match.group(0)
        # Table rows with vectors like [-0.0800, -0.1300, 0.2100]
        if '[' in chunk and ']' in chunk:
            # Pad positive decimals with \phantom{-}
            chunk = re.sub(r'(?<![-\}\d.])(\d+\.\d+)', r'\\phantom{-}\1', chunk)
            # Add padding before ]
            chunk = chunk.replace(']', r'\;]')
        return chunk
        
    text = re.sub(r'^\|.*\|$', process_table_row, text, flags=re.MULTILINE)
    
    # 3. Pad column vectors and matrices correctly
    def process_bmatrix(match):
        chunk = match.group(0)
        
        # If it's a row vector like \begin{bmatrix} 0.35 & -0.17 & -0.27 \end{bmatrix}^\top
        # we do NOT pad it, because they are in different columns and it looks bad.
        # How to detect row vector? It has no '\\' for newlines (except maybe at the end? No, just no \\)
        if '\\\\' not in chunk:
            return chunk # Don't pad row vectors
            
        # For matrices and column vectors, we pad positive decimals
        # But we must be careful with \mathbf{0.2100} -> \phantom{-}\mathbf{0.2100}
        
        # Split by lines
        lines = chunk.split('\n')
        new_lines = []
        for line in lines:
            # pad positive decimals
            new_line = re.sub(r'(?<![-\}\d.])(\d+\.\d+)', r'\\phantom{-}\1', line)
            # fix mathbf
            new_line = new_line.replace(r'\mathbf{\phantom{-}', r'\phantom{-}\mathbf{')
            new_lines.append(new_line)
            
        return '\n'.join(new_lines)

    text = re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}', process_bmatrix, text, flags=re.DOTALL)
    
    # 4. We also need to fix the font size in the summary tables.
    # The user asked to reduce it by another size. Currently it's 0.95em. Let's make it 0.85em.
    text = text.replace('font-size: 0.95em;', 'font-size: 0.85em;')
    
    with open(filepath, 'w') as f:
        f.write(text)

files = glob.glob('/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/*.md')
for f in files:
    clean_and_pad(f)

print("Fixed padding globally")
