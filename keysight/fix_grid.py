with open('architecture.html', 'r') as f:
    html = f.read()

old_css = """    .arch-button-row {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }"""
new_css = """    .arch-button-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 1rem;
    }
    @media (max-width: 900px) {
      .arch-button-row {
        grid-template-columns: 1fr;
      }
    }"""

html = html.replace(old_css, new_css)
with open('architecture.html', 'w') as f:
    f.write(html)
