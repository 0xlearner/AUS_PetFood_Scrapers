import httpx
from selectolax.parser import HTMLParser
import asyncio
import math
import json
import re
import pandas as pd

from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()


class MyPetWareHouse:

    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Connection": "keep-alive",
        # 'Cookie': 'BVBRANDID=26d83d7c-11a7-43b5-ad83-6fd99081d76f; BVBRANDSID=8d95f594-e96d-42a0-8f15-e15bff9fbb2e; PHPSESSID=cpjj0tmib19u2h3ldnpve4t3gcpkv8ar5g9gvkatv8c29bev; BVImplmain_site=17430',
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    async def fetch_urls(self, client, url):

        print(f"Fetching product urls from: {url}", end="")
        response = await client.get(url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        html = HTMLParser(response.text)
        raw_product_urls = [
            "https://www.mypetwarehouse.com.au" + link.attributes["href"]
            for link in html.css("a.list-item-link")
        ]
        product_urls = list(dict.fromkeys(raw_product_urls))
        return product_urls

    async def parse_product_details(self, client, product_url: str):
        item = {}
        print(f"Parsing product details from: {product_url}", end="")
        response = await client.get(product_url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        html = HTMLParser(response.text)
        item["Scraped_Date"] = now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0]
        item["Scraped_Time"] = now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1]
        item["Product_URL"] = html.css_first('meta[property="og:url"]').attributes[
            "content"
        ]
        item["Product_ID"] = product_url.split("-")[-1]
        product_name = (
            html.css_first("h1.p-product-title_.h3_.theme-font_.mt5").text().strip()
        )
        item["Product_Name"] = product_name
        try:
            item["Weight"] = re.search(r"\d+ ?(kg|g)$", product_name.lower()).group(0)
        except:
            item["Weight"] = ""
        item["SKU"] = html.css_first('[itemprop="sku"]').text()
        item["UPC"] = html.css_first('[itemprop="gtin"]').text()
        item["Brand"] = html.css_first('meta[property="og:brand"]').attributes[
            "content"
        ]
        item["Price"] = html.css_first("span.text-price").text()
        try:
            item["Rating"] = html.css_first('[itemprop="ratingValue"]').text()
            item["Reviews"] = html.css_first('[itemprop="reviewCount"]').text()
        except:
            item["Rating"] = "N/A"
            item["Reviews"] = "N/A"
        item["Availability"] = html.css_first('[itemprop="availability"]').text()

        self.results.append(item)

    def to_csv(self):
        df = pd.DataFrame(self.results)
        df.to_csv("mypetwarehouse.csv", index=False)
        print('Stored results to "mypetwarehouse.csv"')

    async def run(self):
        categories = ["dog-food", "dog-treats"]
        async with httpx.AsyncClient(timeout=30) as client:
            for cat in categories:
                for page in range(1, 3):
                    products = await self.fetch_urls(
                        client,
                        f"https://www.mypetwarehouse.com.au/{cat}?page={page}",
                    )
                    tasks = [
                        asyncio.create_task(self.parse_product_details(client, url))
                        for url in products
                    ]

                    await asyncio.gather(*tasks)

                    self.to_csv()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scraper = MyPetWareHouse()
    scraped_data = loop.run_until_complete(scraper.run())
