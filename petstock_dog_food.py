import requests
import pandas as pd
import os
from datetime import datetime
from datetime import date
import json

now = datetime.now()
today = date.today()


class PetStockScraper:

    all_info = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Content-Type": "application/json",
        "Origin": "https://www.petstock.com.au",
        "Connection": "keep-alive",
        "Referer": "https://www.petstock.com.au/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        "siteId": "hgffl8",
        "resultsFormat": "native",
        "bgfilter.collection_id": "185088311432",  # dog_food
        "page": "2",
        "resultsPerPage": "16",
    }

    json_data = {
        "data": {
            "skus": "",
            "warehouses": [
                "1099",
            ],
        },
    }

    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url, params=self.params, headers=self.headers)
        print(f" | Status Code: {res.status_code}")
        return res

    def pagination(self, response):
        json_blob = response.json()
        total_pages = json_blob["pagination"]["totalPages"]

        for page_no in range(1, total_pages + 1):
            self.params["page"] = page_no
            url = "https://api.searchspring.net/api/search/search.json"
            print(f"HTTP GET request page {page_no} to URL: {url}", end="")
            resp = requests.get(url, params=self.params, headers=self.headers)

            self.parse(resp)

    def parse(self, response):
        json_blob = response.json()
        product = [
            {
                "Scraped_Date": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0],
                "Scraped_Time": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1],
                "product_name": d["name"],
                "handle": d["handle"],
                "brand": d["brand"],
            }
            for d in json_blob["results"]
        ]
        variants = [
            json.loads(
                variant["variants"].replace("\\&quot;", "").replace("&quot;", '"')
            )
            for variant in json_blob["results"]
        ]
        for idx, var in enumerate(variants):
            product[idx]["product_id"] = [v["product_id"] for v in var]
            product[idx]["sku"] = [v["sku"] for v in var]
            product[idx]["barcode"] = [v["barcode"] for v in var]
            product[idx]["size"] = [v["option1"] for v in var]
            product[idx]["price"] = [v["price"] for v in var]
            for sku in product[idx]["sku"]:
                self.json_data["data"]["skus"] = sku
                availability_response = requests.post(
                    "https://connector.petstock.io/api/inventory",
                    headers=self.headers,
                    json=self.json_data,
                )
                try:
                    check_availability = float(
                        availability_response.json()["data"][0]["stock"][0]["available"]
                    )

                    if check_availability > 0.0:
                        product[idx]["availability"] = "Available"

                    else:
                        product[idx]["availability"] = "Out of Stock"
                except:
                    product[idx]["availability"] = "Unavailable Online"
        self.to_csv(product)

    def to_csv(self, results):
        df = (
            pd.DataFrame(results)
            .fillna("")
            .explode(["product_id", "size", "price", "sku", "barcode"])
        )

        csv_file = "petstock_dog_food.csv"
        if not os.path.isfile(csv_file):
            df.to_csv(csv_file, index=False)
        else:
            df.to_csv(csv_file, mode="a", encoding="utf-8", header=False, index=False)

        print('Stored results to "petstock_dog_food.csv"')

    def run(self):
        # for page_no in range(1, self.total_pages + 1):
        #     self.params["page"] = page_no
        url = "https://api.searchspring.net/api/search/search.json"

        init_response = self.fetch(url)

        self.pagination(init_response)

        # self.parse(response)


if __name__ == "__main__":
    scraper = PetStockScraper()
    scraper.run()
