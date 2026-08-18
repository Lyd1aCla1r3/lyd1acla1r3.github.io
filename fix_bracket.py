import re

chap5_path = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/chapter_05.md'
with open(chap5_path, 'r') as f:
    text = f.read()

# First, revert the bad replacement
text = text.replace(r'q\'_2[1\;]', r"q'_2[1]")
text = text.replace(r'q\'_2[0\;]', r"q'_2[0]")

# Wait, let's just revert ALL \;] to ] first, then properly apply it only inside tables.
text = text.replace(r'\;]', ']')

# Now apply ONLY to table rows (lines starting with |)
def pad_table_bracket(match):
    chunk = match.group(0)
    # inside a table row, replace any digit followed by ] with digit \; ]
    return re.sub(r'(\d+)]', r'\1\;]', chunk)

text = re.sub(r'^\|.*\|$', pad_table_bracket, text, flags=re.MULTILINE)

with open(chap5_path, 'w') as f:
    f.write(text)

print("Fixed bracket padding")
