import csv
import httpx
import asyncio
import json
import re
from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()


class BudgetPetproducts:

    results = []

    headers = {
        "authority": "www.budgetpetproducts.com.au",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en,ru;q=0.9",
        # 'cookie': '_ALGOLIA=anonymous-6d2b7032-518b-4da0-b0b9-964e00920f3d; scarab.visitor=%2245DBAC5A87F9C262%22; _fbp=fb.2.1674782859328.577366252; _tt_enable_cookie=1; _ttp=jTkn1Rm860eDgPiXlG45pfHRDG7; _gid=GA1.3.415748101.1675529773; _ga_6YGE1ZKCTV=GS1.1.1675616811.3.1.1675617858.0.0.0; _ga=GA1.3.583864494.1674782855; _uetsid=d505d7e0a4ac11ed962a7de239a71ea1; _uetvid=c75d7e109de111eda4efb3023338d7ad; scarab.profile=%2210450%7C1675617860%7C7738%7C1675617847%7C7740%7C1675617814%7C1650%7C1675617803%7C8787%7C1675617792%7C1677%7C1675617770%7C1679%7C1675608652%7C3624%7C1675146623%22; _gat_UA-18961063-1=1; XSRF-TOKEN=eyJpdiI6IkQ4dHJuMjRMeWhyM1pRUi9CS3lZaVE9PSIsInZhbHVlIjoid0IwYzVXY3AxNUN0aG1hYmIzVFNlblIrOTVteEYrMVNQbm9jbTRWTVpWSFhDQUlNRFEraWxJa0tHZC9SRHAyOGZWRnVzZDZlUzBUSlZtUlRBS3hqalVRcStHR0FlZm5ZUTA0STNtRlRpTjFWNlVXM0JEVURvOVhhcjFJeUxEakEiLCJtYWMiOiJmYTNkZTFjMTI1YTA3MjQ1MjZiODM2YWIzMDQ1MTUzODNiZWRlNmYzMWE1N2U3ODhlYzc3OGFlNmMwYmU3ZTE2In0%3D; budget_pet_products_session=eyJpdiI6InI5Q2JvYmliUGNjOTI3Z3EwaUc0YlE9PSIsInZhbHVlIjoiOTJIa3FTZFlzRFpKY29oaVk5NDVES0p6cFFUUlJoNVNVKzJncWdqdVFUeTJ3YVFZSms2aFIwMDRFZm9JSGY0ay92QTdJQjlwcW5ZenVWa1JrV3ZjTmxGUlpwVCttSDBNYWwydUY0WFgxSER3WWROZDlwTVBiakg5K2pNTWVhU1IiLCJtYWMiOiJkYTE2ZGZiODJjYzA5NzAwNDIzNTljOGZlODY3ZDFkYzE0YmY4OTFmODlkZjNjMTE0ZDA4YjE0OTZhZTc0NTcyIn0%3D',
        "referer": "https://www.budgetpetproducts.com.au/dog/food?sort=best_match",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "x-xsrf-token": "eyJpdiI6IkQ4dHJuMjRMeWhyM1pRUi9CS3lZaVE9PSIsInZhbHVlIjoid0IwYzVXY3AxNUN0aG1hYmIzVFNlblIrOTVteEYrMVNQbm9jbTRWTVpWSFhDQUlNRFEraWxJa0tHZC9SRHAyOGZWRnVzZDZlUzBUSlZtUlRBS3hqalVRcStHR0FlZm5ZUTA0STNtRlRpTjFWNlVXM0JEVURvOVhhcjFJeUxEakEiLCJtYWMiOiJmYTNkZTFjMTI1YTA3MjQ1MjZiODM2YWIzMDQ1MTUzODNiZWRlNmYzMWE1N2U3ODhlYzc3OGFlNmMwYmU3ZTE2In0=",
    }

    params = {
        "ajax": "1",
        "filter": "",
        "page": "2",
        "sort": "best_match",
    }

    def striphtml(self, data):
        p = re.compile(r"<.*?>")
        return p.sub("", data)

    async def fetch_urls(self, client, url, params):

        print(f"Fetching product urls from: {url}", end="")
        response = await client.get(url, params=params, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        if response.json()["data"]:
            product_urls = [link["link"] for link in response.json()["data"]["data"]]

            return product_urls
        return "No products!"

    async def parse_product_details(self, client, product_url: str):
        print(f"Parsing product details from: {product_url}", end="")
        response = await client.get(product_url, headers=self.headers)
        print(f" | Status code: {response.status_code}")

        json_blob = json.loads(response.text)["data"]
        try:
            rr_price = json_blob["info"]["prices"]["srp"].split(" ")[-1]
        except:
            rr_price = "N/A"
        if len(json_blob["variances"]):
            product_data = json_blob["variances"][0]["options"]
            product = [
                {
                    "Scraped_Date": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0],
                    "Scraped_Time": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1],
                    "Product_Id": prod["id"],
                    "Product_Slug": prod["name"]["slug"],
                    "Product_Name": prod["name"]["title"],
                    "Product_Size": prod["value"],
                    "Offer_Price": prod["prices"]["price"],
                    "Recommended_Price": prod["prices"]["srp"],
                }
                for prod in product_data
            ]

        else:
            product = [
                {
                    "Scraped_Date": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0],
                    "Scraped_Time": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1],
                    "Product_Id": json_blob["info"]["id"],
                    "Product_Slug": json_blob["info"]["name"]["slug"],
                    "Product_Name": json_blob["info"]["name"]["title"],
                    "Offer_Price": json_blob["info"]["prices"]["price"],
                    "Recommended_Price": rr_price,
                }
            ]
        desc = json_blob["descriptions"]
        for idx, prod in enumerate(product):

            for d in desc:
                if "Description" in d["type"]:
                    product[idx]["Description"] = (
                        self.striphtml(d["description"])
                        .replace("\n", "")
                        .replace("\r", "")
                        .replace("&nbsp;", "")
                    )
                if "Ingredient List" in d["type"]:
                    product[idx]["Ingredients"] = (
                        self.striphtml(d["description"])
                        .replace("\n", "")
                        .replace("\r", "")
                        .replace("&nbsp;", "")
                    )
                if "Feeding Guide" in d["type"]:
                    product[idx]["Feeding_Guide"] = (
                        self.striphtml(d["description"])
                        .replace("\n", "")
                        .replace("\r", "")
                        .replace("&nbsp;", "")
                    )
            product[idx]["Brand"] = json_blob["info"]["brand"]["name"]
            product[idx]["Reviews_Count"] = json_blob["reviews"]["total_reviews"][
                "total"
            ]

            product[idx]["Rating"] = json_blob["reviews"]["average_rating"]

            if product[idx]["Recommended_Price"]:
                product[idx]["Recommended_Price"] = product[idx][
                    "Recommended_Price"
                ].split(" ")[-1]

            # for review in json_blob["reviews"]["reviews"]:
            #     product[idx]["Review_Title"] = review["title"]
            #     product[idx]["Recommend"] = review["subtitle"]
            #     product[idx]["Review_Date"] = review["date"]
            #     product[idx]["Review_Rating"] = review["rating"]
            #     product[idx]["Review_Text"] = review["review"]
        # item["Review_Title"] = [r["title"] for r in json_blob["reviews"]["reviews"]]
        # item["Recommend"] = [r["subtitle"] for r in json_blob["reviews"]["reviews"]]
        # item["Review_Date"] = [r["date"] for r in json_blob["reviews"]["reviews"]]
        # item["Review_Rating"] = [r["rating"] for r in json_blob["reviews"]["reviews"]]
        # item["Review_Text"] = [r["review"] for r in json_blob["reviews"]["reviews"]]
        print(product)
        self.results.append(product)
        self.to_csv()

    def to_csv(self):
        fieldnames = [
            "Product_Id",
            "Product_Slug",
            "Brand",
            "Product_Name",
            "Product_Size",
            "Offer_Price",
            "Recommended_Price",
            "Description",
            "Ingredients",
            "Feeding_Guide",
            "Reviews_Count",
            "Rating",
            # "Review_Title",
            # "Recommend",
            # "Review_Date",
            # "Review_Rating",
            # "Review_Text",
        ]
        with open("budgetpet_products.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.results:
                for r in row:
                    writer.writerow(r)

            print('Stored results to "bpp_food.csv"')

    async def run(self):
        urls = [
            "https://www.budgetpetproducts.com.au/dog/food",
            "https://www.budgetpetproducts.com.au/dog/treats",
        ]
        async with httpx.AsyncClient(timeout=30) as client:
            for page in range(1, 2):
                self.params["page"] = page
                for url in urls:
                    products = await self.fetch_urls(
                        client,
                        url,
                        self.params,
                    )
                    tasks = [
                        asyncio.create_task(self.parse_product_details(client, url))
                        for url in products
                    ]

                    await asyncio.gather(*tasks)

                    self.to_csv()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scraper = BudgetPetproducts()
    scraped_data = loop.run_until_complete(scraper.run())
