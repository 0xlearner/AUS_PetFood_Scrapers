import requests
import pandas as pd
import os
import math
from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()


class PetCircleProdScraper:

    all_info = []

    headers = {
        "authority": "www.petcircle.com.au",
        "accept": "*/*",
        "accept-language": "en,ru;q=0.9",
        # 'cookie': 'scarab.visitor=%223BD6E39AE75D56A8%22; _omappvp=jTYFRdZgxeQuh27z28sX2sM9LhebjsmYPg2b8LtHVIPDfCGRQIOF5zi5X1Y7pthmTon6WXSC30mHiCSqbJzcuXkkmLmXUNA0; _fbp=fb.2.1668266371558.75662233; _tt_enable_cookie=1; _ttp=f540d934-699f-47f0-bf72-7d23f2c64ecc; FPID=FPID2.3.vkAmfaYaCoZfrWDl%2BfTkiWgypvc5AQYqmzwEz3t4IQA%3D.1668266371; __zlcmid=1CulN4k5bKx6ogT; session=fd0dfa92-1002-45cd-a323-fce1bde3d407; _hjSessionUser_3086917=eyJpZCI6ImUxYjBiNDMxLTU3NTktNWQzZi05ODQ2LTY1OWE1MjQ2MjBhYSIsImNyZWF0ZWQiOjE2NjgyNjYzNzE2NTAsImV4aXN0aW5nIjp0cnVlfQ==; PCID=-24_93_112_-97_65_-97_67_44_-105_68_-40_32_26_-111_-118_50_; _ncid=fa028013cf9cde41528d6493a302e23a; scarab.profile=%22H6488HG%7C1669102044%7CH603842%7C1669099704%7C10044%7C1668932863%7C10044VO2X%7C1668902049%7CH10404%7C1668900632%7C8608VO2X%7C1668900539%7C22466VO2X%7C1668899290%7C17990VO2X%7C1668887134%7C63281VO2X%7C1668886948%7CRC42670%7C1668881570%7C63281%7C1668869790%7C10341HG%7C1668738515%7CM5158%7C1668733472%7CRC30531%7C1668601022%7CM440245%7C1668266457%22; _ga_PFN63HFEW8=GS1.1.1674400429.18.1.1674400509.60.0.0; _ga_5WTKLBEYQY=GS1.1.1674400431.18.1.1674400509.60.0.0; registerSuccessRedirectUrl=https://www.upwork.com/; JSESSIONID=82339C83DC48F193A863B329F2722ECF; session_next_check_time=1676454780; userLocation={%22state%22:%22NSW%22%2C%22postcode%22:%222000%22%2C%22zoneId%22:%22280%22%2C%22deliveryCode%22:%22SYD%22}; recentTotals={%22shipping%22:%22$0.00%22%2C%22totalQty%22:0%2C%22totalPrice%22:%22$0.00%22%2C%22totalPay%22:%22$0.00%22%2C%22discounts%22:%22$0.00%22%2C%22signedIn%22:false%2C%22name%22:%22%22%2C%22auto%22:false%2C%22status%22:%22okay%22}; emailSubscription=false; smsSubscription=false; _gcl_au=1.1.288368183.1676452985; sv=sc-sa; _gid=GA1.3.1194637304.1676452991; _hjIncludedInSessionSample_3086917=0; _hjSession_3086917=eyJpZCI6IjE5ZjkwZTE3LTRjZjEtNGMzOS1iOGRiLTg2Y2ExMWVhY2QzNCIsImNyZWF0ZWQiOjE2NzY0NTI5OTM2MTUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; tfpsi=ed031a8d-028c-4cd0-a363-d5d4ff093675; FPLC=86%2B900RzsjZJpP9uBekvmQkTHcVqSgquuZAAlmjFSiECDxQNgghUfnWJ1CPJukcj3tRhVa0WZezqzvBPDU3xx9PO0SUa4zpXfnmNhN1dWXCUnOnjymQ9x0H3RQlEbA%3D%3D; _tq_id.TV-45810963-1.e220=8851d7fff16d1c96.1668266372.0.1676453086..; _ga=GA1.1.232962223.1668266371; _ga_GDZZZRQ0CQ=GS1.1.1676452994.19.1.1676453086.60.0.0; _dc_gtm_UA-24878900-1=1',
        "referer": "https://www.petcircle.com.au/dog/treats",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
        "x-correlation-id": "2d2b7464-7fe5-43fe-b0fe-70008709c6ee",
    }

    params = {
        "totalItemShows": "52",
        "orderType": "POINTS_BASED",
        "includeRatingFilter": "true",
        "returnProducts": "true",
        "tags": [
            "dog",
            "food",
        ],
        "minPrice": "1",
        "maxPrice": "637",
        "pageNumber": "2",
        "delivery-code": "SYD",
        "include": "tag-details",
    }

    categories = ["food", "treats"]

    base_url = "https://www.petcircle.com.au/listing"

    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url, params=self.params, headers=self.headers)
        print(f" | Status Code: {res.status_code}")

        return res

    def pagination(self, response):
        json_blob = response.json()
        total_products = json_blob["metadata"]["totalProducts"]
        products_per_page = len(json_blob["products"]["products"])
        total_pages = round(math.ceil(total_products / products_per_page))

        for cat in self.categories:
            for page_no in range(1, total_pages + 1):
                self.params["pageNumber"] = page_no
                self.params["tags"][1] = cat
                url = self.base_url
                print(f"Fetched page {page_no} from category: {cat}", end="\n")
                resp = requests.get(url, params=self.params, headers=self.headers)

                self.parse(resp)

    def parse(self, resp):
        products = resp.json()["products"]["products"]
        for product in products:
            d = {
                "Scraped_Date": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0],
                "Scraped_Time": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1],
                "brand": product["brand"],
                "brandless_name": product["brandlessName"],
                "product_id": product["productId"],
                "product_name": product["productName"],
                "skus": [prod["sku"] for prod in product["productSkus"]],
                "display_name": [
                    prod["displayName"] for prod in product["productSkus"]
                ],
                "auto_delivery_price": [
                    prod["price"]["autoDeliveryPrice"]
                    for prod in product["productSkus"]
                ],
                "recommended_retail_price": [
                    prod["price"]["recommendedRetailPrice"]
                    for prod in product["productSkus"]
                ],
                "rrp_discount_price": [
                    prod["price"]["rrpDiscountPercent"]
                    for prod in product["productSkus"]
                ],
                "single_order_price": [
                    prod["price"]["singleOrderPrice"] for prod in product["productSkus"]
                ],
            }

            self.all_info.append(d)

    def to_csv(self):
        df = (
            pd.DataFrame(self.all_info)
            .fillna("")
            .explode(
                [
                    "skus",
                    "display_name",
                    "auto_delivery_price",
                    "recommended_retail_price",
                    "rrp_discount_price",
                    "single_order_price",
                ]
            )
        )

        csv_file = f"{today}_petcircle_products.csv"
        if not os.path.isfile(csv_file):
            df.to_csv(csv_file, index=False)
        else:
            df.to_csv(csv_file, mode="a", encoding="utf-8", header=False, index=False)

        print('Stored results to "petcircle_products.csv"')

    def run(self):
        init_response = self.fetch(self.base_url)

        self.pagination(init_response)

        self.to_csv()


if __name__ == "__main__":
    scraper = PetCircleProdScraper()
    scraper.run()
