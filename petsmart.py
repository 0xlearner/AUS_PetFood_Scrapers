import requests
from bs4 import BeautifulSoup
import csv
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

    def fetch_ids(self, url: str):
        print(f"Fetching product ID's from: {url}", end="")
        response = requests.get(url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "lxml")
        json_text = [
            id["data-gtm-product-click"]
            for id in soup.find_all("div", {"class": "product-tile"})
        ]
        prod_ids = [json.loads(j)["id"] for j in json_text]

        return prod_ids

    def parse_product_details(self, product_url: str):
        item = {}
        response = requests.get(product_url, headers=self.headers)
        data = response.json()
        item["Product"] = data["name"]
        try:
            item["Flavor"] = data["variation_values"]["customFlavor"]
        except Exception as e:
            print(f"{product_url} does not have {e}")
            item["Flavor"] = "N/A"
        item["1lbs"] = "N/A"
        item["1.5lbs"] = "N/A"
        item["2lbs"] = "N/A"
        item["5lbs"] = "N/A"
        item["6lbs"] = "N/A"
        for var in data["variants"]:
            if "1 Lb" in var["variation_values"]["size"]:
                item["1lbs"] = var["price"]
            if "1.5 Lb" in var["variation_values"]["size"]:
                item["1.5lbs"] = var["price"]
            if "2 Lb" in var["variation_values"]["size"]:
                item["2lbs"] = var["price"]
            if "5 Lb" in var["variation_values"]["size"]:
                item["5lbs"] = var["price"]
            if "6 Lb" in var["variation_values"]["size"]:
                item["6lbs"] = var["price"]
        try:
            item["Grain_Free"] = (
                "Yes" if "Grain Free" in data["c_customNutritionalOption"] else "No"
            )
        except Exception as e:
            print(f"{product_url} does not have {e}")
            item["Grain_Free"] = "N/A"
        description = [
            d.strip()
            for d in re.sub("<[^<]+?>", " ", html.unescape(data["long_description"]))
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
        with open("petsmart.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "petsmart.csv"')

    def run(self):
        base_url = "https://www.petsmart.com/dog/food/fresh-food/freshpet/?pmin=0.01&srule=best-sellers&format=ajax"
        product_ids = self.fetch_ids(base_url)

        for product_id in product_ids:
            url = f"https://www.petsmart.com/dw/shop/v18_8/products/{product_id}?client_id=11d422c1-e017-4692-8ade-c0d36191da29&expand=prices,variations,availability,promotions,options"
            self.parse_product_details(url)

        self.to_csv()


if __name__ == "__main__":
    scraper = PetSmart()
    scraper.run()
