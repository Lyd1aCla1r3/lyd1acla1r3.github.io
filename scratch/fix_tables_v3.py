import re

with open('blog/content/series/tokenization/chapter_03.md', 'r') as f:
    lines = f.readlines()

out_lines = []
in_table = False

for i, line in enumerate(lines):
    if line.strip().startswith('|---|') or line.strip().startswith('|:---'):
        continue # Skip existing delimiter rows
        
    if line.strip() == '| | |': # Skip existing empty headers
        continue
        
    if line.strip().startswith('| `n</w>` |'):
        # Final vocab table
        if not in_table:
            out_lines.append('\n')
            out_lines.append('| Tokens | | | | |\n')
            out_lines.append('|:---|:---|:---|:---|:---|\n')
            in_table = True
        out_lines.append(line)
        continue
    elif line.strip().startswith('| `walked</w>` |'):
        out_lines.append(line)
        continue

    if 'occurrence' in line and line.strip().startswith('|'):
        if not in_table:
            out_lines.append('\n')
            out_lines.append('| Tokens | Frequency |\n')
            out_lines.append('|:---|---:|\n')
            in_table = True
            
        parts = [p.strip() for p in line.split('|')[1:-1]]
        # In case the table is already 2 columns, parts will have length 2.
        # But if it has empty columns, it might be longer.
        # Let's just extract all code blocks and the occurrence string
        tokens = [p for p in parts if '`' in p]
        occurrence = [p for p in parts if 'occurrence' in p][0]
        
        token_str = ' '.join(tokens)
        out_lines.append(f"| {token_str} | {occurrence} |\n")
        
    elif 'Step ' in line and r'$\rightarrow$' in line and line.strip().startswith('|'):
        if not in_table:
            out_lines.append('\n')
            out_lines.append('| Step | Operation | Result |\n')
            out_lines.append('|:---|:---|---:|\n')
            in_table = True
            
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) >= 5:
            step = parts[0]
            t1 = parts[1]
            plus = parts[2]
            t2 = parts[3]
            arrow_res = parts[4]
            out_lines.append(f"| {step} | {t1} {plus} {t2} | {arrow_res} |\n")
        else:
            # Already formatted properly?
            out_lines.append(line)
            
    else:
        in_table = False
        out_lines.append(line)

with open('blog/content/series/tokenization/chapter_03.md', 'w') as f:
    f.writelines(out_lines)
