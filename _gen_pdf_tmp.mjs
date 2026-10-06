import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/Users/lydia/.cache/puppeteer/chrome/mac_arm-152.0.7977.42/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  const page = await browser.newPage();
  
  const htmlPath = 'file:///Users/lydia/Desktop/personal/career/resumes/Pedersen_Resume_2026.html';
  await page.goto(htmlPath, {waitUntil: 'networkidle0', timeout: 30000});
  
  await page.pdf({
    path: '/Users/lydia/Desktop/personal/career/resumes/Pedersen_Resume_2026.pdf',
    format: 'Letter',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  console.log('PDF generated successfully');
  await browser.close();
})();
