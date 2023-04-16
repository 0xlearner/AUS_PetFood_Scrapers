import httpx
import json
import csv

from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()


class PetCulture:

    results = []

    cookies = {
        "rec_vis_id": "Jtongn80R5mgtWOQDAhaM",
        "_hp2_props.2913334232": "%7B%7D",
        "_dcid": "dcid.1.1675619251100.970999971",
        "shopify_checkoutId": "gid://shopify/Cart/e58fe1e7271d60b902c449452215d409",
        "shopify_checkoutUrl": "https://store.petculture.com.au/cart/c/e58fe1e7271d60b902c449452215d409",
        "_gcl_au": "1.1.658927203.1675619253",
        "_fbp": "fb.2.1675619254087.2742730",
        "_tt_enable_cookie": "1",
        "_ttp": "Gofu6VJet0ku86A4Own2zjsR70E",
        "_gid": "GA1.3.1628024609.1675721162",
        "_hjSessionUser_2191738": "eyJpZCI6ImMxYWY0MzdjLWU5YWQtNWU5YS04NTI2LTQxMjQ4YjU3NWIyMCIsImNyZWF0ZWQiOjE2NzU2MTkyNTM1NDAsImV4aXN0aW5nIjp0cnVlfQ==",
        "_ref": "true",
        "hp._2_3948": "cp-7",
        "_hjAbsoluteSessionInProgress": "1",
        "_hp2_ses_props.2913334232": "%7B%22r%22%3A%22https%3A%2F%2Fwww.petculture.com.au%2Fcollections%2Fdog-food%3Fpage%3D1%22%2C%22ts%22%3A1675733694730%2C%22d%22%3A%22www.petculture.com.au%22%2C%22h%22%3A%22%2Fcollections%2Fdog-food%22%2C%22q%22%3A%22%3Fpage%3D1%22%7D",
        "_hjIncludedInSessionSample": "1",
        "_hjSession_2191738": "eyJpZCI6IjJlOTczZGEyLTQ1ZDktNDk3ZC1hZTUwLTJiMDI5MmVhNDBiYSIsImNyZWF0ZWQiOjE2NzU3MzM2OTkxNzksImluU2FtcGxlIjp0cnVlfQ==",
        "_hjIncludedInPageviewSample": "1",
        "edr-state": "ZUxLJmBOaxoKE-2CO2KRx",
        "_gat_UA-182523077-1": "1",
        "_ga_19YH1HDE4D": "GS1.1.1675733697.4.1.1675733826.0.0.0",
        "_ga": "GA1.3.1835076483.1675619251",
        "_hp2_id.2913334232": "%7B%22userId%22%3A%227953582439516858%22%2C%22pageviewId%22%3A%227018624525232959%22%2C%22sessionId%22%3A%228913694839335589%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D",
        "stape_klaviyo_viewed_items": "%5B%7B%22Title%22%3A%22Royal%20Canin%20Maxi%20Puppy%20Dry%20Dog%20Food%22%2C%22ItemId%22%3A%225892088168608%22%2C%22Categories%22%3A%5B%22Dog%20Food%22%5D%2C%22Url%22%3A%22https%3A%2F%2Fwww.petculture.com.au%2Fproducts%2Froyal-canin-maxi-puppy-dry-dog-food-SKU-000041%3Fcollection%3Ddog-food%22%2C%22Metadata%22%3A%7B%22Brand%22%3A%22ROYAL%20CANIN%22%2C%22Price%22%3A%22139.99%22%7D%2C%22Views%22%3A1%2C%22LastViewedDate%22%3A1675733708%7D%2C%7B%22Title%22%3A%22Black%20Hawk%20Adult%20Dry%20Dog%20Food%20Lamb%20%26%20Rice%22%2C%22ItemId%22%3A%225892197908640%22%2C%22Categories%22%3A%5B%22Dog%20Food%22%5D%2C%22Url%22%3A%22https%3A%2F%2Fwww.petculture.com.au%2Fproducts%2Fblack-hawk-adult-dog-lamb-rice-SKU-001566%3Fcollection%3Ddog-food%22%2C%22Metadata%22%3A%7B%22Brand%22%3A%22BLACK%20HAWK%22%2C%22Price%22%3A%22139.99%22%7D%2C%22Views%22%3A1%2C%22LastViewedDate%22%3A1675733827%7D%5D",
        "_uetsid": "e74933d0a66a11ed9e4ee785a1d8a09b",
        "_uetvid": "2b3d3c30a57d11edb34a273975070d96",
        "_dd_s": "rum=1&id=105cf3a4-3620-4ac1-8856-05a8f06ec1bd&created=1675733687307&expire=1675734734493",
    }

    headers = {
        "authority": "www.petculture.com.au",
        "accept": "*/*",
        "accept-language": "en,ru;q=0.9",
        # 'cookie': 'rec_vis_id=Jtongn80R5mgtWOQDAhaM; _hp2_props.2913334232=%7B%7D; _dcid=dcid.1.1675619251100.970999971; shopify_checkoutId=gid://shopify/Cart/e58fe1e7271d60b902c449452215d409; shopify_checkoutUrl=https://store.petculture.com.au/cart/c/e58fe1e7271d60b902c449452215d409; _gcl_au=1.1.658927203.1675619253; _fbp=fb.2.1675619254087.2742730; _tt_enable_cookie=1; _ttp=Gofu6VJet0ku86A4Own2zjsR70E; _hjSessionUser_2191738=eyJpZCI6ImMxYWY0MzdjLWU5YWQtNWU5YS04NTI2LTQxMjQ4YjU3NWIyMCIsImNyZWF0ZWQiOjE2NzU2MTkyNTM1NDAsImV4aXN0aW5nIjp0cnVlfQ==; _ref=true; stape_klaviyo_viewed_items=%5B%7B%22Title%22%3A%22Royal%20Canin%20Maxi%20Puppy%20Dry%20Dog%20Food%22%2C%22ItemId%22%3A%225892088168608%22%2C%22Categories%22%3A%5B%22Dog%20Food%22%5D%2C%22Url%22%3A%22https%3A%2F%2Fwww.petculture.com.au%2Fproducts%2Froyal-canin-maxi-puppy-dry-dog-food-SKU-000041%3Fcollection%3Ddog-food%22%2C%22Metadata%22%3A%7B%22Brand%22%3A%22ROYAL%20CANIN%22%2C%22Price%22%3A%22139.99%22%7D%2C%22Views%22%3A1%2C%22LastViewedDate%22%3A1675733708%7D%2C%7B%22Title%22%3A%22Black%20Hawk%20Adult%20Dry%20Dog%20Food%20Lamb%20%26%20Rice%22%2C%22ItemId%22%3A%225892197908640%22%2C%22Categories%22%3A%5B%22Dog%20Food%22%5D%2C%22Url%22%3A%22https%3A%2F%2Fwww.petculture.com.au%2Fproducts%2Fblack-hawk-adult-dog-lamb-rice-SKU-001566%3Fcollection%3Ddog-food%22%2C%22Metadata%22%3A%7B%22Brand%22%3A%22BLACK%20HAWK%22%2C%22Price%22%3A%22139.99%22%7D%2C%22Views%22%3A1%2C%22LastViewedDate%22%3A1675733827%7D%5D; hp._2_3948=cp-13; _gid=GA1.3.1147784989.1676298373; _hp2_id.2913334232=%7B%22userId%22%3A%227953582439516858%22%2C%22pageviewId%22%3A%226024523325942255%22%2C%22sessionId%22%3A%228611995530129707%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; __gtm_referrer=; _ga_19YH1HDE4D=GS1.1.1676304244.8.0.1676304244.0.0.0; _ga=GA1.1.1835076483.1675619251; _hp2_ses_props.2913334232=%7B%22ts%22%3A1676304243771%2C%22d%22%3A%22www.petculture.com.au%22%2C%22h%22%3A%22%2F_next%2Fdata%2FJHtsvxybFyzeiLoEUTCda%2Fproducts%2Fstockman-paddock-working-dog-dry-dog-food-SKU-004686.json%22%7D; _uetsid=5e1f4450abaa11eda7e151372de79ff2; _uetvid=2b3d3c30a57d11edb34a273975070d96; _hjIncludedInSessionSample_2191738=1; _hjSession_2191738=eyJpZCI6IjY0ZjQyNjc3LTkyN2UtNDBiMi05NTIzLThjMjQ3NWQ4ZTk2ZCIsImNyZWF0ZWQiOjE2NzYzMDQyNDY2NzQsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0',
        "if-none-match": 'W/"xlmvgysak62kvo"',
        "purpose": "prefetch",
        "referer": "https://www.petculture.com.au/collections/dog-food?page=3",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
        "x-nextjs-data": "1",
    }

    params = {
        "collection": "dog-food",
        "slug": "black-hawk-adult-dog-lamb-rice-SKU-004141",
    }

    categories = ["dog-food", "dog-treats", "puppy-food"]

    base_url = "https://cq45c0coif-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.11.3)%3B%20react%20(18.2.0)%3B%20react-instantsearch%20(6.38.3)&x-algolia-api-key=30f78909ba0ca139096a649889583a26&x-algolia-application-id=CQ45C0COIF"

    def fetch_product_listing(self, url: str, post_data):
        print(f"Fetching product ID's from: {url}", end="")
        response = httpx.post(self.base_url, headers=self.headers, data=post_data)
        print(f" | Status code: {response.status_code}")
        products = response.json()["results"][0]["hits"]
        product_urls = [
            "https://www.petculture.com.au/_next/data/IdFk6Eaj1E884YEjjZ91U/products/"
            + url["handle"]
            + "-"
            + url["sku"]
            + ".json"
            for url in products
        ]

        return product_urls

    def fetch_product_details(self, API_URL: str, params):
        print(f"Fetching product from: {API_URL}", end="")
        response = httpx.get(
            API_URL, params=params, cookies=self.cookies, headers=self.headers
        )
        print(f" | Status code: {response.status_code}")
        if response.status_code == 200:
            product_info = response.json()["pageProps"]["product"]
            variants = response.json()["pageProps"]["product"]["variants"]

            product = [
                {
                    "Scraped_Date": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0],
                    "Scraped_Time": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1],
                    "SKU": v["sku"],
                    "Product_Variant": v["fullVariantTitle"],
                    "Size": v["name"],
                    "Price": v["price"],
                    "Availability": v["availableForSale"],
                }
                for v in variants
            ]

            try:
                ingredients = (
                    product_info["nutritionInfo"]["ingredients"]
                    .replace("\n", "")
                    .replace("\r", "")
                )
            except:
                ingredients = "N/A"

            for idx, _ in enumerate(product):
                product[idx]["Product_Name"] = product_info["name"]
                product[idx]["Slug"] = product_info["slug"]
                product[idx]["Description"] = product_info["description"]
                product[idx]["Ingredients"] = ingredients
                product[idx]["Rating"] = product_info["reviewScore"]
                product[idx]["Reviews"] = product_info["reviewCount"]

            self.results.append(product)
            self.to_csv()

    def to_csv(self):
        fieldnames = [
            "Scraped_Time",
            "Scraped_Date",
            "SKU",
            "Product_Name",
            "Slug",
            "Product_Variant",
            "Size",
            "Price",
            "Description",
            "Ingredients",
            "Rating",
            "Reviews",
            "Availability",
        ]
        with open("petculture.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.results:
                for r in row:
                    writer.writerow(r)

            print('Stored results to "petculture.csv"')

    def run(self):
        for page in range(0, 63):
            for cat in self.categories:
                data = f"""{{"requests":[{{"indexName":"shopify_pc1_products","params":"clickAnalytics=true&facetFilters=%5B%5B%22collections%3A{cat}%22%5D%5D&facets=%5B%22collections%22%2C%22grams%22%2C%22tags%22%2C%22collection_ids%22%2C%22vendor%22%2C%22named_tags.categories%22%2C%22price%22%2C%22named_tags.breed%20size%22%2C%22named_tags.benefits%22%2C%22named_tags.lifestyle%22%2C%22named_tags.life%20stage%22%2C%22inventory_available%22%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=16&maxValuesPerFacet=50&page={page}&query=&tagFilters="}},{{"indexName":"shopify_pc1_products","params":"analytics=false&clickAnalytics=false&facets=collections&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=50&page=0&query="}}]}}"""
                print(data)
                products = self.fetch_product_listing(
                    self.base_url,
                    data,
                )
                for prod in products:
                    self.params["collection"] = cat
                    self.params["slug"] = prod.split("/")[-1].split(".")[0]
                    self.fetch_product_details(prod, self.params)


if __name__ == "__main__":
    scraper = PetCulture()
    scraper.run()
