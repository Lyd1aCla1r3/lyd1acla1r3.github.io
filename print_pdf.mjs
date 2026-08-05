import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Use file protocol for local file
  const htmlPath = 'file:///Users/lydia/Desktop/personal/career/resumes/Pedersen_Resume_2026.html';
  await page.goto(htmlPath, {waitUntil: 'networkidle0'});
  
  await page.pdf({
    path: '/Users/lydia/Desktop/personal/career/resumes/Pedersen_Resume_2026.pdf',
    format: 'Letter',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  await browser.close();
})();
