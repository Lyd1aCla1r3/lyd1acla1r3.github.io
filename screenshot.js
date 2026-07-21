const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({width: 1440, height: 900});

  await page.goto('http://localhost:8000/index.html');
  await page.screenshot({path: 'screenshot_index.png'});

  await page.goto('http://localhost:8000/blog/index.html');
  await page.screenshot({path: 'screenshot_blog.png'});

  await browser.close();
})();
