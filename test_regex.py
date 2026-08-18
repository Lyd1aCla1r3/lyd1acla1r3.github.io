import re
import glob

def pad_positive_numbers(text):
    # Match any number like 0.12 or 1.0000 that is NOT preceded by a minus sign or phantom
    # We use a negative lookbehind for - and } (from \phantom{-})
    # Also we don't want to pad numbers inside tags or other constructs, but mostly these are plain numbers.
    # A safer way is to find all matrix blocks and table lines.
    
    # Let's write a function to process a chunk of math text
    def process_math(match):
        chunk = match.group(0)
        # Find all decimal numbers
        # (?<![-\}\d.]) \d+\.\d+
        # Negative lookbehind: not preceded by -, }, digit, or .
        chunk = re.sub(r'(?<![-\}\d.])(\d+\.\d+)', r'\\phantom{-}\1', chunk)
        return chunk
    
    # Process all bmatrix environments
    text = re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}', process_math, text, flags=re.DOTALL)
    
    # Process all markdown table rows that look like they contain vectors
    # e.g., | [ ... ] | [ ... ] |
    def process_table_row(match):
        chunk = match.group(0)
        if '[' in chunk and ']' in chunk:
            chunk = re.sub(r'(?<![-\}\d.])(\d+\.\d+)', r'\\phantom{-}\1', chunk)
        return chunk
        
    text = re.sub(r'^\|.*\|$', process_table_row, text, flags=re.MULTILINE)
    
    return text

# Test on a snippet
snippet = r" \begin{bmatrix} 0.35 & -0.17 \\ 1.20 & \phantom{-}0.50 \end{bmatrix} "
print("Before:", snippet)
print("After:", pad_positive_numbers(snippet))

