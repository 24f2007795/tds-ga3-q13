import asyncio
from playwright.async_api import async_playwright

async def get_sum(page, url):
    await page.goto(url)

    # wait for table to load (dynamic content)
    await page.wait_for_selector("table")
    await page.wait_for_timeout(1000)

    return await page.evaluate("""
        () => {
            let total = 0;
            const tables = document.querySelectorAll('table');
            for (const table of tables) {
                const cells = table.querySelectorAll('td, th');
                for (const cell of cells) {
                    const text = cell.innerText.trim();
                    if (/^-?[0-9]+(\\.[0-9]+)?$/.test(text)) {
                        total += parseFloat(text);
                    }
                }
            }
            return total;
        }
    """)

async def main():
    seeds = range(6, 16)  # 78 to 87
    total_sum = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            s = await get_sum(page, url)
            total_sum += s

        await browser.close()

    print(f"TOTAL_SUM={total_sum}")  # IMPORTANT FORMAT

if __name__ == "__main__":
    asyncio.run(main())
