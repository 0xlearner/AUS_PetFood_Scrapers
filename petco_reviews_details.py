import httpx
import asyncio
from urllib.parse import unquote
from datetime import datetime
import math
import json
import re
import pandas as pd


class PetCoReviews:

    results = []

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en,ru;q=0.9",
        "Connection": "keep-alive",
        "Origin": "https://www.petco.com",
        "Referer": "https://www.petco.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    }

    params = {
        "c": "ciojs-client-2.29.9",
        "key": "key_afiSr5Y4gCaaSW5X",
        "i": "0eddac8c-e39b-4207-91fe-9ea6ca58365e",
        "s": "8",
        "page": "2",
        "num_results_per_page": "48",
        "sort_by": "relevance",
        "sort_order": "descending",
        "variations_map": '{"dtype":"object","values":{"minPrice":{"aggregation":"min","field":"data.offerprice"},"maxPrice":{"aggregation":"max","field":"data.offerprice"}}}',
        "_dt": "1674810999783",
    }

    review_params = {
        "resource.q0": "reviews",
        "filter.q0": [
            "productid:eq:5054620",
            "contentlocale:eq:en_US,en_US",
            "isratingsonly:eq:false",
        ],
        "filter_reviews.q0": "contentlocale:eq:en_US,en_US",
        "include.q0": "authors,products",
        "filteredstats.q0": "reviews",
        "limit.q0": "30",
        "offset.q0": "38",
        "sort.q0": "submissiontime:desc",
        "passkey": "dpaqzblnfzrludzy2s7v27ehz",
        "apiversion": "5.5",
        "displaycode": "3554-en_us",
    }

    async def fetch_urls(self, client, url):

        print(f"Fetching product urls from: {url}", end="")
        response = await client.get(url, params=self.params, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        product_urls = [
            "https://www.petco.com" + u["data"]["url"]
            for u in response.json()["response"]["results"]
        ]

        return product_urls

    async def fetch_id(self, client, url):

        print(f"Fetching product urls from: {url}", end="")
        response = await client.get(url, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        if response.status_code == 200:
            data = (
                re.search(r"__NEXT_DATA__(.*)", response.text)
                .group(1)
                .replace('" type="application/json">', "")
            )
            json_data = json.loads(data[: data.index("</script>")])
            product_id = json_data["props"]["pageProps"]["initialState"]["product"][
                "parentPartNumber"
            ]

            return product_id

    async def parse_product_reviews(self, client, product_id: str, API_URL: str):
        self.review_params["filter.q0"][0] = f"productid:eq:{product_id}"
        response = await client.get(
            API_URL, params=self.review_params, headers=self.headers
        )
        # print(f"Fetching product review api from: {unquote(response.url)}", end="")
        # print(f" | Status code: {response.status_code}")
        json_blob = response.json()
        total_reviews = round(
            math.ceil(json_blob["BatchedResults"]["q0"]["TotalResults"]) / 8
        )

        for i in range(0, total_reviews):
            item = {}
            review_page = i * 8
            self.review_params["offset.q0"] = review_page
            self.review_params["filter.q0"][0] = f"productid:eq:{product_id}"
            response = await client.get(
                API_URL, params=self.review_params, headers=self.headers
            )
            # print(
            #     f"Fetching paginated product review api from: {unquote(response.url)}",
            #     end="",
            # )
            # print(f" | Status code: {response.status_code}")
            json_blob = response.json()
            product = json_blob["BatchedResults"]["q0"]["Includes"]["Products"][
                f"{product_id}"
            ]
            item["Product_Name"] = product["Name"]
            item["Total_Rating"] = product["FilteredReviewStatistics"][
                "AverageOverallRating"
            ]
            item["User"] = [
                r["UserNickname"] for r in json_blob["BatchedResults"]["q0"]["Results"]
            ]
            item["Time"] = [
                datetime.fromisoformat(r["SubmissionTime"]).date().strftime("%m-%d-%Y")
                for r in json_blob["BatchedResults"]["q0"]["Results"]
            ]
            item["Heading"] = [
                r["Title"] for r in json_blob["BatchedResults"]["q0"]["Results"]
            ]
            item["Detail"] = [
                r["ReviewText"] for r in json_blob["BatchedResults"]["q0"]["Results"]
            ]
            item["Recommend"] = []
            for recommend in json_blob["BatchedResults"]["q0"]["Results"]:
                if recommend["IsRecommended"] == True:
                    item["Recommend"].append("Y")
                else:
                    item["Recommend"].append("N")
            item["No_helpful_vote"] = product["FilteredReviewStatistics"][
                "NotHelpfulVoteCount"
            ]
            item["Yes_helpful_vote"] = product["FilteredReviewStatistics"][
                "HelpfulVoteCount"
            ]
            print(item)
            self.results.append(item)

    def to_csv(self):
        df = (
            pd.DataFrame(self.results)
            .fillna("")
            .explode(["User", "Time", "Heading", "Detail", "Recommend"])
        )
        df.to_csv("petco_reviews_details.csv", index=False)
        print('Stored results to "petco_reviews_details.csv"')

    async def run(self):
        async with httpx.AsyncClient(timeout=30) as client:
            for page in range(1, 5):
                self.params["page"] = page
                product_urls = await self.fetch_urls(
                    client,
                    "https://ac.cnstrc.com/browse/group_id/dry-dog-food",
                )
                api_url = "https://api.bazaarvoice.com/data/batch.json"
                prod_ids = []
                for url in product_urls:
                    prod_ids.append(await self.fetch_id(client, url))
                tasks = [
                    asyncio.create_task(
                        self.parse_product_reviews(client, prod_id, api_url)
                    )
                    for prod_id in prod_ids
                ]

                await asyncio.gather(*tasks)

                self.to_csv()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scraper = PetCoReviews()
    scraped_data = loop.run_until_complete(scraper.run())
