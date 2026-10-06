import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Use file protocol for local file
  const htmlPath = 'file:///Users/lydia/Desktop/personal/career/resumes/portfolio/blog/serp-api-benchmark.html';
  await page.goto(htmlPath, {waitUntil: 'networkidle0'});
  
  await page.pdf({
    path: '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/serp-api-benchmark.pdf',
    format: 'Letter',
    printBackground: true,
    preferCSSPageSize: true
  });

  await browser.close();
})();
