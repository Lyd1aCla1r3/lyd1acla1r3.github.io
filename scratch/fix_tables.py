import re

with open('blog/content/series/tokenization/chapter_03.md', 'r') as f:
    lines = f.readlines()

out_lines = []
in_corpus_table = False
in_merge_table = False

for line in lines:
    if line.startswith('|---|'):
        continue
    
    if line.startswith('| `n</w>` | `talked</w>` |'):
        # Final vocab table, leave it alone but remove it from corpus/merge processing
        out_lines.append('| | | | | |\n')
        out_lines.append('|---|---|---|---|---|\n')
        out_lines.append(line)
        continue
    elif line.startswith('| `walked</w>` | `walker</w>` |'):
        out_lines.append(line)
        continue

    if '1 occurrence' in line:
        if not in_corpus_table:
            out_lines.append('| | |\n')
            out_lines.append('|---|---|\n')
            in_corpus_table = True
        
        # Parse tokens
        parts = [p.strip() for p in line.split('|')[1:-1]]
        tokens = [p for p in parts if p.startswith('`')]
        occurrence = [p for p in parts if 'occurrence' in p][0]
        
        token_str = ' '.join(tokens)
        out_lines.append(f"| {token_str} | {occurrence} |\n")
    
    elif 'Step ' in line and '$\rightarrow$' in line:
        if not in_merge_table:
            out_lines.append('| | | | |\n')
            out_lines.append('|---|---|---|---|\n')
            in_merge_table = True
            
        parts = [p.strip() for p in line.split('|')[1:-1]]
        step = parts[0]
        t1 = parts[1]
        plus = parts[2]
        t2 = parts[3]
        arrow_result = parts[4].split('$\rightarrow$')
        arrow = '$\rightarrow$'
        result = arrow_result[1].strip()
        
        expr = f"{t1} {plus} {t2}"
        out_lines.append(f"| {step} | {expr} | {arrow} | {result} |\n")
        
    elif line.startswith('| | |'):
        # Skip header rows for tables we are rewriting
        continue
    else:
        in_corpus_table = False
        in_merge_table = False
        out_lines.append(line)

with open('blog/content/series/tokenization/chapter_03.md', 'w') as f:
    f.writelines(out_lines)
