from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio


async def get_site_cookies(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        cookies_list = await page.context.cookies()
        cookies_dict = {el["name"]: el["value"] for el in cookies_list}
        await browser.close()

    return cookies_dict


url = "https://www.woolworths.com.au/shop/browse/pet/dog-puppy"
cookies = asyncio.run(get_site_cookies(url))
print(cookies)
