import sys
PLAN = '/Users/lydia/.gemini/antigravity/brain/628163fe-9db3-499c-9b7f-f47c1314aafa/si_ebook_revision_plan.md'

with open(PLAN, 'r') as f:
    text = f.read()

# Replace S14 status
old_s14 = "| S14 | P-BUILD, P-VERIFY | Blog rebuild, v2.0 PDF, visual verification, final checkpoint | **Gate:** user final review | TODO |"
new_s14 = "| S14 | P-BUILD, P-VERIFY | Blog rebuild, v2.0 PDF, visual verification, final checkpoint | **Gate:** user final review | DONE (Gate: awaiting user final review) |"

text = text.replace(old_s14, new_s14)

# Append to Status Tracker
# The status tracker table ends before the "## 9. Decision Log" or similar.
# Let's just append at the end of the Status Tracker table.
# Find the end of the Status Tracker table.

lines = text.split('\n')
new_lines = []
in_tracker = False
for line in lines:
    new_lines.append(line)
    if "### 10.3 Status Tracker" in line:
        in_tracker = True
    elif in_tracker and line.startswith("## ") or (in_tracker and line == "---"):
        # We reached the end of the tracker/next section (Wait, there are carry-over notes after the tracker, not a new heading)
        pass

# A better way is to insert right after the S13 row in the Status Tracker, but S13 isn't clearly marked in the tracker table since I didn't see it when I read the truncated file... wait, S13 is P-IMG.
