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

    # headers = {
    #     "authority": "api.searchspring.net",
    #     "accept": "*/*",
    #     "accept-language": "en,ru;q=0.9",
    #     "origin": "https://www.petstock.com.au",
    #     "referer": "https://www.petstock.com.au/",
    #     "sec-ch-ua": '"Chromium";v="106", "Yandex";v="22", "Not;A=Brand";v="99"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": '"Linux"',
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "cross-site",
    #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.832 (beta) Yowser/2.5 Safari/537.36",
    # }

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
        "filter.vendor": "SPD Air",
        # "bgfilter.collection_id": "185088213128", # dog
        # "bgfilter.collection_id": "185088311432", # dog_food
        "page": "2",
        "resultsPerPage": "16",
        # "q": "prime",
        "q": "air dried",
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

        csv_file = "petstock_dog_air_dried.csv"
        if not os.path.isfile(csv_file):
            df.to_csv(csv_file, index=False)
        else:
            df.to_csv(csv_file, mode="a", encoding="utf-8", header=False, index=False)

        print('Stored results to "petstock.csv"')

    def run(self):
        for page_no in range(1, 2):
            self.params["page"] = page_no
            url = "https://api.searchspring.net/api/search/search.json"

            response = self.fetch(url)

            self.parse(response)


if __name__ == "__main__":
    scraper = PetStockScraper()
    scraper.run()
