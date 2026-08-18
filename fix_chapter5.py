import re
import os
import glob

# 1. Fix Chapter 5 specific paragraph deletion and table font size
chap5_path = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/chapter_05.md'
with open(chap5_path, 'r') as f:
    text = f.read()

paragraph_to_remove = "The rotation has substantially altered the first two components. The original $\mathbf{q}_1$ had $q_1[0] = 0.35$ (positive) and $q_1[1] = -0.17$ (negative). After rotation by 1 radian, $q'_1[1]$ has become positive ($0.2027$), and $q'_1[0]$ has changed only slightly ($0.35 \\to 0.3322$). The third component is unchanged because dimension 2 is unpaired."

text = text.replace(paragraph_to_remove + "\n", "")
text = text.replace(paragraph_to_remove, "")

# 2. Add padding before ] in the tables
# We look for vectors like: [-0.0800,\; -0.1300,\; \phantom{-}0.2100]
# and replace ] with \;]
text = re.sub(r'(\d+)]', r'\1\;]', text)

# 3. Add font-size reduction for the summary tables
query_table_header = "| Position | Token | $\mathbf{q}_t$ (before RoPE) | $\mathbf{q}'_t$ (after RoPE) |"
new_query_table_header = "<div style=\"font-size: 0.95em; overflow-x: auto;\">\n\n" + query_table_header
if query_table_header in text and "<div" not in text:
    text = text.replace(query_table_header, new_query_table_header)
    
    # We need to close the div after the table.
    # The table ends before "## Applying RoPE to the Key Vectors"
    text = text.replace("## Applying RoPE to the Key Vectors", "</div>\n\n## Applying RoPE to the Key Vectors")

key_table_header = "| Position | Token | $\mathbf{k}_t$ (before RoPE) | $\mathbf{k}'_t$ (after RoPE) |"
new_key_table_header = "<div style=\"font-size: 0.95em; overflow-x: auto;\">\n\n" + key_table_header
if key_table_header in text and "<div" not in text.split("## Applying RoPE to the Key Vectors")[-1]:
    text = text.replace(key_table_header, new_key_table_header)
    # The table is at the end of the file or before another section.
    # Actually, let's just append </div> at the end of the file since it's the last thing.
    text = text + "\n</div>\n"

with open(chap5_path, 'w') as f:
    f.write(text)

print("Fixed Chapter 5")
