# lydia pedersen — portfolio

Documentation Engineer & AI Pipeline Architect

[**→ View Live Portfolio**](https://lyd1acla1r3.github.io)

---

## About

This repository contains the source code for my professional portfolio. It showcases my technical writing samples, AI pipeline architecture case studies, and the documentation engineering systems I've designed and built.

The site is a hand-crafted static portfolio built with semantic HTML5, vanilla CSS, and vanilla JavaScript. No frameworks, no build tools, no dependencies. The constraint is the feature: the portfolio itself is a demonstration of my approach to documentation engineering — clean, accessible, well-structured, and maintainable.

## Structure

```
.
├── index.html              # Single-page portfolio
├── css/
│   └── styles.css          # Design system and component styles
├── js/
│   └── main.js             # Navigation, animations, and interactions
├── assets/
│   ├── images/             # Headshot and architecture diagrams
│   └── docs/               # Downloadable writing samples (PDF)
└── README.md
```

## Sections

| Section | Description |
|---------|-------------|
| **Hero** | Introduction, professional title, and contact links |
| **About** | Career narrative and key metrics |
| **Writing Samples** | 10 curated documentation samples from Gravitee and Entando, with PDF downloads and category filters |
| **Documentation Engineering** | 4 AI pipeline case studies with architecture diagrams — abstract, clean-room descriptions with no proprietary code |
| **Skills** | Technical competencies organized by domain |
| **Contact** | Email, GitHub, and LinkedIn links |

## Writing Samples

All writing samples are original documentation I authored. PDFs are snapshots of my published work:

**Gravitee (2023–2026):** Configure the Kafka Client & Gateway, Gravitee Expression Language, Gateway Resource Sizing, Connect to an Endpoint Using SSE, Docker CLI

**Entando (2021–2023):** Getting Started with Entando, Standard Banking Demo, Strapi Content Management, Entando Multitenancy, Manage NGINX

## Case Studies

The pipeline case studies describe systems I designed and built at Gravitee. These are architectural overviews — no proprietary source code is included:

- **AI Doc Writer Agent** — Multi-stage content generation from PR diffs to publication-ready docs
- **Analytics Deflection Engine** — 9-step pipeline transforming AI assistant analytics into documentation improvement reports
- **Link Governance Engine** — 19-category link classifier with safety-gated autofix
- **Semantic Redirect Engine** — Embedding-based cross-version page mapping

## Technical Details

- **Typography:** Inter (body) + JetBrains Mono (code/labels) via Google Fonts
- **Design:** Dark theme with blue/teal/purple/amber accents
- **Accessibility:** Semantic HTML, ARIA labels, skip navigation, keyboard-navigable
- **Performance:** No build step, no JavaScript frameworks, no runtime dependencies
- **Responsive:** Mobile-first with breakpoints at 480px, 768px, and 1024px

## Local Development

```bash
# Serve locally (Python 3)
python3 -m http.server 8000

# Then open http://localhost:8000
```

## License

Content © Lydia Pedersen. Writing samples remain the intellectual property of their respective companies (Gravitee, Entando) and are shared here for portfolio purposes only.
