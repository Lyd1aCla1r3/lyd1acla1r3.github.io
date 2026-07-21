import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({width: 1440, height: 900});

  await page.goto('http://localhost:8000/blog/serp-api-benchmark.html', {waitUntil: 'networkidle2'});
  await page.screenshot({path: 'screenshot_article.png'});

  await browser.close();
})();
