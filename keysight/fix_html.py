with open('architecture.html', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    # We messed up the buttons replacement by leaving extra </div> tags.
    # Let's clean up everything inside the arch-card-content blocks.
    pass
