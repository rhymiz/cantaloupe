import { test, expect } from '@playwright/test';

test('Google Search', async ({ page }) => {
    await page.goto('https://www.google.com');
    await page.locator('blablal').click();
    if (new RegExp("/*.store/").test(page.url)) {
  alert("has");
}

    await page.screenshot({'timeout': 1})
    await page.goto('https://www.google.com');
    await page.locator('input[title="Search"]').click();
    await page.locator('input[title="Search"]').type('rhymiz');
    await page.locator('input[value="Google Search"] >> nth=0').click();
    const boo = page.locator('input');
    if (boo.count() === 3) {
      alert("aye baybay!")
}

    await page.locator('select[name="country"]').selectOption({'label': 'US'});
    await page.locator('select[name="country"]').selectOption([{'label': 'US'}, {'label': 'CA'}]);
    await page.getByTitle('GO', {'timeout': 1});
    await page.reload();
    
});