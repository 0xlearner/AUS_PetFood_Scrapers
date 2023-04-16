import httpx
from bs4 import BeautifulSoup
import json
import re
import math
import csv
from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()


class PetBarnProdScraper:

    all_info = []

    headers = {
        "authority": "www.petbarn.com.au",
        "accept": "*/*",
        "accept-language": "en,ru;q=0.9",
        "content-type": "application/json",
        # 'cookie': 'form_key=H4T0fcvSEeqWdLtR; PHPSESSID=c1514aa75719bd4bccae91b4bd378715; _hjSessionUser_697727=eyJpZCI6ImMxZTQzZDE0LWJiMDAtNThlNi05YThhLTFlODcxMWQ3NWQwNSIsImNyZWF0ZWQiOjE2NjgyNjY5MDAyNTMsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.1814422308.1673680421; s_ecid=MCMID%7C14352294586015616793216407977341736282; aam_uuid=19481282441348406572612417380699116100; _fbp=fb.2.1673680424775.13195942; mage-messages=; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; mage-cache-sessid=true; product-selected-swatch-options=%7B%7D; changeYoutubeCode=; _pin_unauth=dWlkPU16Y3dNbVF6T0dNdE1tWTBOaTAwWTJSa0xUazVZakV0TXprek5XWm1ZV014WWprMw; catURL=https%3A%2F%2Fwww.petbarn.com.au%2Fdogs%2Fdog-food%2Fdry-dog-food%3Fp%3D2%26product_list_order%3Dposition; _gid=GA1.3.487573837.1676308468; at_check=true; AMCVS_CAFC1FE55D6CC83E0A495E73%40AdobeOrg=1; AMCV_CAFC1FE55D6CC83E0A495E73%40AdobeOrg=-1124106680%7CMCIDTS%7C19402%7CMCMID%7C14352294586015616793216407977341736282%7CMCAID%7CNONE%7CMCOPTOUT-1676323464s%7CNONE%7CMCAAMLH-1676921064%7C3%7CMCAAMB-1676921064%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-19405%7CvVersion%7C5.2.0; s_cc=true; catURL=https%3A%2F%2Fwww.petbarn.com.au%2Fdogs%2Fdog-food; s_vnc365=1707857253856%26vn%3D14; s_ivc=true; s_inv=4991; _hjIncludedInSessionSample_697727=0; _hjSession_697727=eyJpZCI6IjllMGI4MmRkLTVmZGYtNDYzOC04YzM5LTBkYzQ3MjliYmRlNSIsImNyZWF0ZWQiOjE2NzYzMjEyNTU2MjMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; private_content_version=8276dff7bc33f11c405f5e6827d1e4e7; section_data_ids=%7B%22live_chat%22%3A1676321260%2C%22autocomplete-address%22%3A1676321264%2C%22pickup-store%22%3A1676321271%2C%22launch%22%3A1676321271%7D; _gat_UA-27528868-1=1; _derived_epik=dj0yJnU9Z0c1UldBaTBlY196RTNCdHBna183dzFrNl9ncTVDTkcmbj1qNmNVVUdBZElqbTlXS2hGT2FuYTNRJm09MSZ0PUFBQUFBR1Bxb2pvJnJtPTEmcnQ9QUFBQUFHUHFvam8mc3A9Mg; _uetsid=e1d18f30abc111ed96e1992bd0e783d1; _uetvid=aa29f960629e11edafaa2973a52bbfa2; s_sq=%5B%5BB%5D%5D; gpv_Page=petbarn%3Aleaps-bounds-kangaroo-large-breed-adult-dog-food-15kg; s_nr30=1676321361031-Repeat; s_tslv=1676321361039; BE_CLA3=p_id%3DLAR2J2448244RJ2NP22N4J6N8AAAAAAAAH%26bn%3D15%26bv%3D3.45%26s_expire%3D1676407761198%26s_id%3DLAR2J2448244R2N8JJ8N4J6N8AAAAAAAAH; _ga_BW9RWVMF8W=GS1.1.1676321251.16.1.1676321361.24.0.0; _ga=GA1.3.298394843.1673680423; mbox=PC#613a8353cdab419e8249b9f573c8eae8.38_0#1739566163|session#569fb89887f04707a71aebc6c05681d3#1676323223',
        "origin": "https://www.petbarn.com.au",
        "referer": "https://www.petbarn.com.au/leaps-bounds-kangaroo-large-breed-adult-dog-food-15kg",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
        "x-newrelic-id": "VgMAVlRWCRAEVllTDwQBV1E=",
        "x-requested-with": "XMLHttpRequest",
    }

    def fetch_base_url(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        response = httpx.get(url, timeout=30)
        print(f" | Status Code: {response.status_code}")

        return response

    def next_url(self, url, response):
        soup = BeautifulSoup(response.text, "html.parser")
        total_products = int(soup.select_one("span.toolbar-number.total-number").text)
        products_per_page = int(soup.select("span.toolbar-number")[1].text)
        total_pages = round(math.ceil(total_products / products_per_page))

        for page in range(2, total_pages + 1):
            next_url = url + f"?p={str(page)}"
            print(f"Fetching page: {next_url}", end=" ")
            next_response = httpx.get(next_url, timeout=30)
            self.parse_product_info(next_response)

    def parse_product_info(self, response):
        datalayer = (
            re.search(r"adobeDatalayerEvent = (.*)", response.text)
            .group(1)
            .replace(";", "")
        )
        products = json.loads(datalayer)
        product_list = json.loads(products[0])["PLP"]["products"]
        breadcrumb = json.loads(products[0])["PLP"]["productBreadcrumbs"]
        product_skus = [sku["productSKU"] for sku in product_list]
        product_data = []
        json_data = {
            "query": f"query {{ products (filter: {{ sku: {{ in: {json.dumps(product_skus)}}}}}) {{    items {{      id sku thumbnail {{ url label }} member_price ...on ConfigurableProduct {{ variants {{ attributes {{ uid label code }} product {{ id sku  thumbnail {{ url label }} member_price price_range {{ minimum_price {{ final_price {{value}} regular_price {{value}} }} }} }} }} }} price_range {{ minimum_price {{ final_price {{value}} regular_price {{value}} }} }} }} }} }}"
        }

        api_response = httpx.post(
            "https://www.petbarn.com.au/graphql",
            headers=self.headers,
            json=json_data,
        )
        data = api_response.json()["data"]["products"]["items"]
        for pl in product_list:
            for d in data:
                if d:
                    if pl["productSKU"] == d["sku"]:
                        if "variants" in d:
                            for v in d["variants"]:
                                product_data.append(
                                    {
                                        "scraped_date": now.strftime(
                                            "%m/%d/%Y, %H:%M:%S"
                                        ).split(",")[0],
                                        "scraped_time": now.strftime(
                                            "%m/%d/%Y, %H:%M:%S"
                                        ).split(",")[1],
                                        "product_name": pl["productName"],
                                        "product_sku": d["sku"],
                                        "variant_sku": v["product"]["sku"],
                                        "product_weight": v["attributes"][0]["label"],
                                        "category": "-".join(breadcrumb.split("-")[1:]),
                                        "member_price": v["product"]["member_price"],
                                        "regular_price": v["product"]["price_range"][
                                            "minimum_price"
                                        ]["regular_price"]["value"],
                                        "final_price": v["product"]["price_range"][
                                            "minimum_price"
                                        ]["final_price"]["value"],
                                        "life_stage": pl["lifeStage"],
                                    }
                                )
                        else:
                            try:
                                product_name = pl["productName"]
                                product_weight = re.search(
                                    r"\d+ ?(kg|g)$", product_name.lower()
                                ).group(0)
                            except:
                                product_weight = "N/A"
                            product_data.append(
                                {
                                    "scraped_date": now.strftime(
                                        "%m/%d/%Y, %H:%M:%S"
                                    ).split(",")[0],
                                    "scraped_time": now.strftime(
                                        "%m/%d/%Y, %H:%M:%S"
                                    ).split(",")[1],
                                    "product_name": pl["productName"],
                                    "product_sku": d["sku"],
                                    "variant_sku": "N/A",
                                    "product_weight": product_weight,
                                    "category": "-".join(breadcrumb.split("-")[1:]),
                                    "member_price": d["member_price"],
                                    "regular_price": d["price_range"]["minimum_price"][
                                        "regular_price"
                                    ]["value"],
                                    "final_price": d["price_range"]["minimum_price"][
                                        "final_price"
                                    ]["value"],
                                    "life_stage": pl["lifeStage"],
                                }
                            )
        self.all_info.append(product_data)
        self.to_csv()

    def to_csv(self):
        fieldnames = [
            "scraped_date",
            "scraped_time",
            "product_name",
            "product_sku",
            "variant_sku",
            "product_weight",
            "category",
            "member_price",
            "regular_price",
            "final_price",
            "life_stage",
        ]
        with open("petbarn_products.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.all_info:
                for r in row:
                    writer.writerow(r)

            print('Stored results to "petbarn_products.csv"')

    def run(self):
        cat_urls = [
            "https://www.petbarn.com.au/dogs/dog-treats",
            "https://www.petbarn.com.au/dogs/dog-food/raw-fresh-frozen",
            "https://www.petbarn.com.au/dogs/brand/prime100",
            "https://www.petbarn.com.au/dogs/dog-food/dry-dog-food",
        ]
        for url in cat_urls:
            response = self.fetch_base_url(url)
            self.parse_product_info(response)
            self.next_url(url, response)


if __name__ == "__main__":
    scraper = PetBarnProdScraper()
    scraper.run()
