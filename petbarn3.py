import requests
from bs4 import BeautifulSoup
import json
import re
import csv


class PetBarnProdScraper:

    all_info = []

    def fetch_base_url(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url)
        print(f" | Status Code: {res.status_code}")

        return res

    def fetch_product_links(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        raw_urls = [link.get("href") for link in soup.select("a.product-item-link")]
        product_urls = [p for p in raw_urls if p]
        next_page = soup.select_one("li.pages-item-next > a").get("href")

        for url in product_urls:
            self.fetch_product_data(url)
            # if next_page is not None:
            #     self.fetch_product_data(url)

    def fetch_product_data(self, url):
        print(url)
        print(f"Fetching product URL: {url}", end="")
        response = requests.get(url)
        print(f" | Status Code: {response.status_code}")
        soup = BeautifulSoup(response.text, "lxml")
        pdpProductData = re.search(
            r"window.pdpProductData = (.*)", response.text
        ).group(1)
        clean_pd = re.sub("<[^<]+?>", "", pdpProductData).replace(";", "")
        prod_data = json.loads(clean_pd)
        size_data = soup.select_one('script[type="application/ld+json"]')
        if "children" in prod_data:
            product = [
                {
                    "product_id": prod_data["children"][key]["id"],
                    "product_sku": prod_data["children"][key]["sku"],
                    "product_name": prod_data["children"][key]["name"],
                }
                for key in prod_data["children"].keys()
            ]

        if "children" not in prod_data:
            product = [
                {
                    "product_id": prod_data["id"],
                    "product_sku": prod_data["sku"],
                    "product_name": prod_data["name"],
                }
            ]

        # html_json = re.search(r"window.odProductConfig = (.*)", response.text).group(1)
        # json_str = re.sub("<[^<]+?>", "", html_json).replace(";", "")
        # json_blob = json.loads(json_str)
        data = soup.select_one("script:-soup-contains('[data-role=swatch-options]')")
        for idx, prod_id in enumerate(product):

            if data is not None:
                json_blob = json.loads(data.text.replace("\n", ""))
                price_block = json_blob["[data-role=swatch-options]"][
                    "Magento_Swatches/js/swatch-renderer"
                ]["jsonConfig"]["optionPrices"]
                price_html = price_block[prod_id]["rendered_price"]
                price_soup = BeautifulSoup(price_html, "html.parser")
                price_selector = f"span#product-price-{prod_id}"
                product[idx]["regular_price"] = price_soup.select_one(
                    price_selector
                ).get("data-price-amount")
                member_price_selector = price_soup.select_one(
                    "div.price-box.member-price"
                )
                if member_price_selector:
                    product[idx]["member_price"] = member_price_selector.text.strip()
            # if "regular_price" in main_entity:
            #     product[idx]["regular_price"] = main_entity["regular_price"]
            # if "member_price" in main_entity:
            #     product[idx]["member_price"] = main_entity["member_price"]
            # if "save_amount" in main_entity:
            #     product[idx]["save_amount"] = main_entity["save_amount"]

            for tr in soup.select("tbody"):
                row = tr.select("tr")
                for td in row:
                    table_heading = td.select_one("th")
                    if table_heading is not None:
                        if (
                            table_heading.text != "Member Price"
                            and table_heading.text != "Benefits"
                            and table_heading.text != "Size"
                            and table_heading.text != "Feeding Guide"
                            and table_heading.text != "Weight Control"
                            and table_heading.text != "Activity Level"
                        ):
                            table_data = td.select_one("td")
                            if table_data is not None:
                                product[idx][table_heading.text] = (
                                    table_data.text.replace("•  ", "")
                                    .replace("\n", "")
                                    .strip()
                                )

            if size_data:
                size_json_text = size_data.text.replace(
                    '<script type="application/ld+json">', ""
                ).replace("</script>", "")
                size_json_blob = json.loads(size_json_text)["offers"]
                if "offers" in size_json_blob:
                    for s in size_json_blob["offers"]:
                        if s["sku"] == prod_id["product_sku"]:
                            product[idx]["product_size"] = s["size"]
                elif size_json_blob["sku"] == prod_id["product_sku"]:
                    product[idx]["product_size"] = size_json_blob["size"]

        # print(product)
        self.all_info.append(product)
        self.to_csv()

        # print(product)

    def to_csv(self):
        fieldnames = [
            "product_id",
            "product_sku",
            "product_name",
            "regular_price",
            "member_price",
            # "save_amount",
            "product_size",
            "Product Category",
            "Treat Type",
            "Food Type",
            "Advice Care",
            "Brand",
            "Flavour",
            "Ingredients",
            "Nutrition Grade",
            "Breed",
            "Life Stage",
            "Health Benefits",
            "Australia Made",
            "Health Condition Dietary",
        ]
        with open("petbarn_dry.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.all_info:
                for r in row:
                    writer.writerow(r)

            print('Stored results to "petbarn_dry.csv"')

    def run(self):
        # url = f"https://www.petbarn.com.au/dogs/dog-treats"
        # url = f"https://www.petbarn.com.au/dogs/dog-food/raw-fresh-frozen?p={i}"
        # url = f"https://www.petbarn.com.au/dogs/brand/prime100"
        url = f"https://www.petbarn.com.au/dogs/dog-food/dry-dog-food"

        response = self.fetch_base_url(url)
        self.fetch_product_links(response)
        # for i in range(1, 3):  # total_number of pages
        #     # url = f"https://www.petbarn.com.au/dogs/dog-treats?p={i}"
        #     # url = f"https://www.petbarn.com.au/dogs/dog-food/raw-fresh-frozen?p={i}"
        #     url = f"https://www.petbarn.com.au/dogs/brand/prime100?p={i}"
        #     # url = f"https://www.petbarn.com.au/dogs/dog-food/dry-dog-food?p={i}"

        #     response = self.fetch_base_url(url)
        #     product_links = self.fetch_product_links(response)

        #     for product_url in product_links:
        #         self.fetch_product_data(product_url)


if __name__ == "__main__":
    scraper = PetBarnProdScraper()
    scraper.run()
