import requests
from bs4 import BeautifulSoup
import csv
import json
from urllib.parse import unquote


class PetSmartReviews:

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

    params = {
        "passkey": "208e3foy6upqbk7glk4e3edpv",
        "apiversion": "5.5",
        "displaycode": "4830-en_us",
        "resource.q0": "reviews",
        "filter.q0": [
            "isratingsonly:eq:false",
            "productid:eq:69272",
            "contentlocale:eq:en,en_US",
        ],
        "sort.q0": "submissiontime:desc",
        "stats.q0": "reviews",
        "filteredstats.q0": "reviews",
        "include.q0": "authors,products,comments",
        "filter_reviews.q0": "contentlocale:eq:en,en_US",
        "filter_reviewcomments.q0": "contentlocale:eq:en,en_US",
        "filter_comments.q0": "contentlocale:eq:en,en_US",
        "limit.q0": "8",
        "offset.q0": "0",
        "limit_comments.q0": "3",
        "callback": "bv_1111_34596",
    }

    def fetch_prod_ids(self, url: str):
        print(f"Fetching product ID's from: {url}", end="")
        response = requests.get(url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "lxml")
        product_ids = [
            link.get("href").split(".")[0].split("-")[-1]
            for link in soup.find_all("a", {"class": "name-link"})
        ]

        return product_ids

    def parse_reviews(self, product_id: str, API_URL: str):
        item = {}
        self.params["filter.q0"][1] = f"productid:eq:{product_id}"
        response = requests.get(API_URL, params=self.params, headers=self.headers)
        print(f"Fetching product review api from: {unquote(response.url)}", end="")
        print(f" | Status code: {response.status_code}")
        start = response.text.index("{")
        end = response.text.rfind(")")
        json_blob = json.loads(response.text[start:end])
        product = json_blob["BatchedResults"]["q0"]["Includes"]["Products"][
            f"{product_id}"
        ]
        item["Product_Name"] = product["Name"]
        item["Total_Rating"] = product["ReviewStatistics"]["AverageOverallRating"]
        item["Total_Reviews"] = product["TotalReviewCount"]
        ratings = product["ReviewStatistics"]["RatingDistribution"]
        for rating in ratings:
            item[f"""{rating['RatingValue']} star"""] = rating["Count"]
        secondary_rating_order = product["ReviewStatistics"][
            "SecondaryRatingsAveragesOrder"
        ]
        for sro in secondary_rating_order:
            item[sro] = product["ReviewStatistics"]["SecondaryRatingsAverages"][sro][
                "AverageRating"
            ]
        self.results.append(item)

    def to_csv(self):
        with open("petsmart_reviews.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "petsmart_reviews.csv"')

    def run(self):
        api_url = "https://api.bazaarvoice.com/data/batch.json"
        base_url = "https://www.petsmart.com/dog/food/fresh-food/freshpet/?pmin=0.01&srule=best-sellers&format=ajax"
        product_ids = self.fetch_prod_ids(base_url)
        for _id in product_ids:
            self.parse_reviews(_id, api_url)
        self.to_csv()


if __name__ == "__main__":
    scraper = PetSmartReviews()
    scraper.run()
