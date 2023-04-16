import httpx
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import html


class PetSmart:

    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
    }

    async def fetch_ids(self, client, url):
        print(f"Fetching product ID's from: {url}", end="")
        response = await client.get(url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "lxml")
        json_text = [
            id["data-gtm-product-click"]
            for id in soup.find_all("div", {"class": "product-tile"})
        ]
        prod_ids = [json.loads(j)["id"] for j in json_text]

        return prod_ids

    async def parse_product_details(self, client, product_url: str):
        item = {}
        print(f"Parsing product details from: {product_url}", end="")
        response = await client.get(product_url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            item["Product"] = data["name"]
            try:
                item["Flavor"] = data["variation_values"]["customFlavor"]
            except Exception as e:
                print(f"{product_url} does not have {e}")
                item["Flavor"] = "N/A"

            for var in data["variants"]:
                item[var["variation_values"]["size"]] = var["price"]
                try:
                    item[f'{var["variation_values"]["size"]}_offer_price'] = data[
                        "prices"
                    ]["ps-us-sale-pricebook"]
                except:
                    item[f'{var["variation_values"]["size"]}_offer_price'] = "N/A"
                item[f'{var["variation_values"]["size"]}_recommended_price'] = data[
                    "prices"
                ]["ps-us-list-pricebook"]
            try:
                item["Grain_Free"] = (
                    "Yes" if "Grain Free" in data["c_customNutritionalOption"] else "No"
                )
            except Exception as e:
                print(f"{product_url} does not have {e}")
                item["Grain_Free"] = "N/A"
            description = [
                d.strip()
                for d in re.sub(
                    "<[^<]+?>", " ", html.unescape(data["long_description"])
                )
                .strip()
                .split("\r\n\r\n")
            ]
            life_stage = [l.strip() for l in description[0].split("\r\n")]
            for stage in life_stage:
                if stage.startswith("Life Stage"):
                    item["Life_Stage"] = stage.split(":")[-1].strip()
            for ingredients in description:
                if ingredients.startswith("Ingredients"):
                    item["Ingredients"] = ingredients.split(":")[-1].strip()
            item["URL"] = product_url
            item["Rating"] = data["c_bvAverageRating"]
            item["Reviews"] = data["c_bvReviewCount"]
            self.results.append(item)

    def to_csv(self):
        df = pd.DataFrame(self.results)
        df.to_csv("petsmart_2.csv", index=False)
        print('Stored results to "petsmart_2.csv"')

    async def run(self):
        async with httpx.AsyncClient(timeout=30) as client:
            for page in range(1, 4):
                page_no = page * 36
                base_url = f"https://www.petsmart.com/dog/food/royal-canin+royal-canin-veterinary-diet/?pmin=0.01&srule=best-sellers&start={page_no}&sz=36&format=ajax"
                product_ids = await self.fetch_ids(client, base_url)
                product_urls = [
                    f"https://www.petsmart.com/dw/shop/v18_8/products/{product_id}?client_id=11d422c1-e017-4692-8ade-c0d36191da29&expand=prices,variations,availability,promotions,options"
                    for product_id in product_ids
                ]

                tasks = [
                    asyncio.create_task(self.parse_product_details(client, url))
                    for url in product_urls
                ]

                await asyncio.gather(*tasks)

                self.to_csv()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scraper = PetSmart()
    scraped_data = loop.run_until_complete(scraper.run())
