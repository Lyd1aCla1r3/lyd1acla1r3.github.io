import re

with open('blog/content/series/tokenization/chapter_03.md', 'r') as f:
    lines = f.readlines()

out_lines = []

def get_freq(step_num):
    if step_num in [1, 2]: return 6
    if step_num == 3: return 4
    if step_num in [4, 5, 6]: return 3
    if 7 <= step_num <= 14: return 2
    return 1

for line in lines:
    stripped = line.strip()
    
    if stripped == '| Tokens | Frequency |':
        out_lines.append('| Tokens |\n')
    elif stripped == '|:---|---:|':
        out_lines.append('|:---|\n')
    elif 'occurrence |' in line or 'occurrences |' in line:
        # It's a corpus data row, e.g., | `w` `a` `k` ... | 1 occurrence |
        parts = [p.strip() for p in line.split('|')[1:-1]]
        tokens = parts[0]
        out_lines.append(f"| {tokens} |\n")
    elif stripped == '| Step | Operation | Result |':
        out_lines.append('| Step | Operation | Result | Frequency |\n')
    elif stripped == '|:---|:---|:---|':
        out_lines.append('|:---|:---|:---|---:|\n')
    elif stripped.startswith('| Step ') and r'$\rightarrow$' in line:
        # Merge data row, e.g., | Step 1 | `a` + `l` | $\rightarrow$ `al` |
        parts = [p.strip() for p in line.split('|')[1:-1]]
        step_str = parts[0]
        op = parts[1]
        res = parts[2]
        
        step_num = int(step_str.replace('Step ', ''))
        freq = get_freq(step_num)
        freq_str = f"{freq} occurrence" if freq == 1 else f"{freq} occurrences"
        
        out_lines.append(f"| {step_str} | {op} | {res} | {freq_str} |\n")
    else:
        out_lines.append(line)

with open('blog/content/series/tokenization/chapter_03.md', 'w') as f:
    f.writelines(out_lines)
