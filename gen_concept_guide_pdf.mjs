import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { marked } from 'marked';

const mdPath = process.argv[2];
const pdfPath = process.argv[3];

if (!mdPath || !pdfPath) {
  console.error('Usage: node gen_concept_guide_pdf.mjs <input.md> <output.pdf>');
  process.exit(1);
}

const md = readFileSync(mdPath, 'utf-8');
const htmlBody = marked.parse(md);

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] },
  svg: { fontCache: 'global' },
  startup: { pageReady: () => MathJax.startup.defaultPageReady().then(() => window.__mathRendered = true) }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  @page { size: letter; margin: 0.7in 0.75in; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 9pt; line-height: 1.55; color: #2a2a2a;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
  h1 {
    font-size: 20pt; font-weight: 800; color: #0071C5;
    border-bottom: 3px solid #0071C5; padding-bottom: 8px;
    margin-bottom: 16px; margin-top: 0; line-height: 1.2;
  }
  h2 {
    font-size: 13pt; font-weight: 700; color: #0071C5;
    border-bottom: 2px solid #0071C5; padding-bottom: 4px;
    margin-bottom: 10px; margin-top: 22px;
  }
  h3 {
    font-size: 10.5pt; font-weight: 700; color: #1a1a1a;
    margin-top: 16px; margin-bottom: 6px;
  }
  p { margin-bottom: 8px; text-align: justify; hyphens: auto; }
  ul, ol { margin-left: 18px; margin-bottom: 8px; }
  li { margin-bottom: 4px; }
  strong { font-weight: 600; }
  em { font-style: italic; }
  code {
    font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
    font-size: 8pt; background: #f4f6f8; padding: 1px 4px;
    border-radius: 3px;
  }
  pre {
    font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
    font-size: 7.5pt; background: #f4f6f8; padding: 10px 14px;
    border-radius: 4px; margin: 8px 0 12px 0; line-height: 1.55;
    overflow-x: hidden; white-space: pre-wrap;
    break-inside: avoid; page-break-inside: avoid;
  }
  pre code { background: none; padding: 0; font-size: inherit; }
  table {
    width: 100%; border-collapse: collapse; margin-bottom: 12px;
    font-size: 8pt; break-inside: avoid; page-break-inside: avoid;
  }
  thead th {
    background: #0071C5; color: white; font-weight: 600;
    text-align: left; padding: 5px 8px; font-size: 7.8pt;
    text-transform: uppercase; letter-spacing: 0.3px;
  }
  tbody td {
    padding: 4px 8px; border-bottom: 1px solid #e0e8f0;
    vertical-align: top; line-height: 1.45;
  }
  tbody tr:nth-child(even) { background: #f6f9fc; }
  hr { border: none; border-top: 1px solid #d0d8e0; margin: 18px 0; }
  mjx-container { overflow-x: auto; }
  .doc-footer {
    margin-top: 24px; text-align: center;
    font-size: 7pt; color: #aaa;
  }
</style>
</head>
<body>
${htmlBody}
<div class="doc-footer">Signal Integrity Fundamentals Concept Guide &bull; Keysight Interview Preparation &bull; September 2026</div>
</body>
</html>`;

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0', timeout: 30000 });
  // Wait for MathJax to finish rendering
  await page.waitForFunction(() => window.__mathRendered === true, { timeout: 15000 }).catch(() => {
    console.warn('MathJax render timeout - proceeding anyway');
  });
  await page.pdf({
    path: pdfPath,
    format: 'Letter',
    printBackground: true,
    preferCSSPageSize: true,
  });
  console.log('PDF generated:', pdfPath);
  await browser.close();
})();
