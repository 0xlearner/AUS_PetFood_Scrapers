import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import pandas as pd


class PetCo:

    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.petco.com/shop/en/petcostore/brand/freshpet",
        "Alt-Used": "www.petco.com",
        "Connection": "keep-alive",
        "Cookie": "Edgescape-Country=PK; Edgescape-City=Karachi; Edgescape-State=Sindh; Edgescape-Zip=74600; Edgescape-Lat=24.85910; Edgescape-Long=66.99830; datadome=0hhWsX5MU9DfGQ5jPuXtIVDCssNRyqrEN2QxMWcMOGY6z2bsdsVESFDaWD7_me~Il-CBGORTy75WBt-IHFf934tEvZ7XEMum9F6xB8VWRLzhSemQy_0ge3YtY-esvJy3; __cf_bm=L8NYQPBMm2rDulMnU22M1rKin46m0Rq.aaYxILjB5GE-1673864255-0-AWbiiOV6VJSnt/KpW/LXRL0pXVrtvUygSPo1zmdxxEOhsRAxujIn2tPzV+mOuRqZLHexMR7MBXD7Kiwq8c15FBGh7Ca/biE+qtJAofQ7ATl4qDVJMuHlk8eOKHckiiyfWNlcxXQBSu0i+cnXAbC62xNBaiSC4kij3HBeGm+kCZDChv11lUVWJh1BkheHauegbxXh8hicXsOHUSAIeY3uGjM=; _cfuvid=bSD3p8Y1X8VTnSZirJulVC.EsxeX3Nl3K0mZpiNvOJQ-1673863929868-0-604800000; AT_RDSN_option=var_B; ConstructorioID_client_id=804fcec0-ba97-47c9-bd54-c0a45a9add75; AMCV_4BED2CAD546FC7A60A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19374%7CMCMID%7C81621503568567409217629165684611765790%7CMCAID%7CNONE%7CMCOPTOUT-1673871611s%7CNONE%7CvVersion%7C5.2.0; mbox=session#e8f8e2ae31cd4adb9b8a069f67dce550#1673866131; at_check=true; s_plt=6.94; s_pltp=undefined; JSESSIONID=00001nnK07SiLYV3T6JMTXDptax:1ckhh37is; AMCVS_4BED2CAD546FC7A60A4C98C6%40AdobeOrg=1; OptanonConsent=isGpcEnabled=1&datestamp=Mon+Jan+16+2023+15%3A17%3A52+GMT%2B0500+(Pakistan+Standard+Time)&version=202210.1.0&hosts=&groups=BG55%3A0%2CCADNS%3A0%2CC0004%3A0%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1&consentId=fab3c3d3-93a6-4e90-8eb5-fbc110011ac2; gpv_Page=product%20display%20page; _cs_mk_aa=0.171929496191628_1673863936783; s_cc=true; WC_bopusStoreId=12356; BVImplmain_site=3554; __rutmb=215766422; __rutma=215766422-21-8z-4h-1p-xslbj1hz1n7ky69s5ip6-1673863940961.1673863940961.1673863940961.1.6.6; __rpck=0!PTAhZXlKME55STZlMzBzSW5RM2RpSTZlMzBzSW1Waklqb3hMQ0owT0NJNmV5SXpJam94Tmpjek9EWTBNalV4TWpFeGZYMH4~; __rpckx=0!eyJ0NyI6eyI0IjoxNjczODY0MjU1NjY3LCI1IjoxNjczODY0MjY3NDAzfSwidDd2Ijp7IjQiOjE2NzM4NjQyNTU2NjcsIjUiOjE2NzM4NjQ4MDg5MTZ9LCJlYyI6M30~; __ruid=215766422-21-8z-4h-1p-xslbj1hz1n7ky69s5ip6-1673863940961; __rcmp=0!bj1fZ2MsZj1nYyxzPTEsYz00NzA5LHRyPTEwMCxybj05OCx0cz0yMDIzMDExNi4xMDEyLGQ9cGM7bj1ydzEsZj1ydyxzPTEsYz0yNzE3LHQ9MjAyMDEyMTQuMTk0NA~~; BVBRANDID=cd9abaeb-0057-4bcd-850d-545755227ee3; BVBRANDSID=5c47d313-ae0c-4b81-a17b-f1e410cb9955; s_sq=petcoprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dproduct%252520display%252520page%2526link%253DINGREDIENTS%252520%252526%252520ANALYSIS%2526region%253D__next%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dpetco.com%25253Aproduct%25253AFreshpet%25253AFreshpet%252520Vital%252520Fresh%252520Cuts%252520Shredded%252520Chicken%252520Dog%252520Food%25252C%2525201.5%252520lbs.%2526pidt%253D1%2526oid%253DINGREDIENTS%252520%252526%252520ANALYSIS%2526oidt%253D3%2526ot%253DSUBMIT; AT_RDSN_option=var_B; WC_PERSISTENT=6w51tVVZOpfbIFdOkKfj1v2XCeAm2O%2FnBj7%2BYNPpT2E%3D%3B2023-01-16+02%3A13%3A46.429_1673864026427-216638_10151_-1002%2C-1%2CUSD%2CXg%2Bitqut0fQsMargAAzSq%2FlsK%2BrCVvVmVSVl%2BrJ4ts4mhiuqBjJhGwFBJiAr%2BtP9epuFuERcMmKiy2TmWzeYaQ%3D%3D_10151; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=-1002%2Czd0Zytk7JKgfHE%2FklIX4v2%2BFwqnndBhSZW%2F9a5Zwf1U%3D; WC_ACTIVEPOINTER=-1%2C10151; WC_USERACTIVITY_-1002=-1002%2C10151%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1902309707%2CN8BOq4CIatHNJkh2AX1TyXtlwlzaTgLj5jkXxLgSrjdExq7BIVwc6eU2ne4ib0iP5zL7URBE1wTE07DxqTC1N9SO8THNHDYcdc%2BuDZYzPJukQ9rP%2FyP80xW92xCysKluyYV5vIb6Q3Bx4EwUwcck%2FA8TS%2BYVqFx4P9%2BQ7jecmc0KizQaFqMlFE0KcQlBw0v9tmSv3iUs5KniNKX5O3tsssHmh%2B4k%2Bk7tOVGrDjANT6HXPLkSUXMzNALKh%2BPLMUuk; WC_GENERIC_ACTIVITYDATA=[56363397556%3Atrue%3Afalse%3A0%3A4bkysKs%2BGL0f6sFDTQJBQcXHUI8vlGDVqEo8cHSEGe4%3D][com.ibm.commerce.context.entitlement.EntitlementContext|10003%2610003%26null%26-2000%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|1673864026427-216638][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10051%26null%26false%26false%26false][com.ibm.commerce.context.experiment.ExperimentContext|null][com.petco.context.PetcoPGRContext|null][com.ibm.commerce.context.ExternalCartContext|null][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10151%26-1002%26-1002%26-1][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; WC_UserType=G; WC_UserId=-1002; rUserType=G; WC_physicalStores=12356%2C12356%2C12356%2C12356%2C12356; RFK_ACCESS_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcGlLZXkvNTVjZjdiYjEiLCJzY29wZSI6eyIyMTU3NjY0MjIiOlsidzZndDQ0OHh1ZyJdfSwic3RhZ2UiOiJwcm9kIiwicmVnaW9uIjoidXMtZWFzdC0xIiwianRpIjoiYTk4YmY3ZGMtMzAxMC00NWQ5LWE0NDctZDE0YjViNjJiMTMwIiwiaWF0IjoxNjczODU4Mzk5LCJleHAiOjE2NzM5NDUzOTl9.qFLezd2nLpsSeSRMr8tl6OkbRa_dwzOEYrTpX16_DFw; priceMode=2; pdp-aa-test=group-a",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
    }

    params = {
        "ajaxStoreImageDir": "/wcsstore/PetcoSAS/",
        "searchType": "12",
        "advancedSearch": "",
        "filterTerm": "",
        "storeId": "10151",
        "manufacturer": "freshpet",
        "ddkey": "ProductListingView_4_3074457345618259661_4099276460824412711",
        "sType": "SimpleSearch",
        "metaData": "",
        "brandSearch": "freshpet",
        "catalogId": "10051",
        "searchTerm": "",
        "resultsPerPage": "48",
        "filterFacet": "",
        "resultCatEntryType": "",
        "gridPosition": "",
        "emsName": "",
        "disableProductCompare": "true",
        "langId": "-1",
        "facet": "",
    }

    def fetch_product_urls(self, url: str):
        print(f"Fetching product urls from: {url}", end="")
        response = requests.get(url, params=self.params, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "lxml")
        product_urls = [
            link.find_next("a")["href"] for link in soup.select("div.product-name")
        ]

        return product_urls

    def parse_product_details(self, product_url: str):
        item = {}
        print(f"Parsing product details from: {product_url}", end="")
        response = requests.get(product_url, params=self.params, headers=self.headers)
        print(f" | Status code: {response.status_code}")
        if response.status_code == 200:
            data = (
                re.search(r"__NEXT_DATA__(.*)", response.text)
                .group(1)
                .replace('" type="application/json">', "")
            )
            json_data = json.loads(data[: data.index("</script>")])
            prod_ids = list(
                json_data["props"]["pageProps"]["initialState"]["product"][
                    "composedItemView"
                ].keys()
            )
            item["Product"] = product_url.split("/")[-1]
            item["Flavor"] = json_data["props"]["pageProps"]["initialState"]["product"][
                "composedItemView"
            ][f"{prod_ids[0]}"]["details"]["table"][2]["text"]

            item["1lbs"] = "N/A"
            item["1.5lbs"] = "N/A"
            item["2lbs"] = "N/A"
            item["5lbs"] = "N/A"
            item["6lbs"] = "N/A"

            for key in prod_ids:
                try:
                    prod_var = json_data["props"]["pageProps"]["initialState"][
                        "product"
                    ]["composedItemView"][f"{key}"]["details"]["table"][5]["text"]

                    if "1 LB" in prod_var:
                        item["1lbs"] = json_data["props"]["pageProps"]["initialState"][
                            "product"
                        ]["composedItemView"][f"{key}"]["price"]["price_USD"]
                    if "1.5 LB" in prod_var:
                        item["1.5lbs"] = json_data["props"]["pageProps"][
                            "initialState"
                        ]["product"]["composedItemView"][f"{key}"]["price"]["price_USD"]
                    if "2 LB" in prod_var:
                        item["2lbs"] = json_data["props"]["pageProps"]["initialState"][
                            "product"
                        ]["composedItemView"][f"{key}"]["price"]["price_USD"]
                    if "5 LB" in prod_var:
                        item["5lbs"] = json_data["props"]["pageProps"]["initialState"][
                            "product"
                        ]["composedItemView"][f"{key}"]["price"]["price_USD"]
                    if "6 LB" in prod_var:
                        item["6lbs"] = json_data["props"]["pageProps"]["initialState"][
                            "product"
                        ]["composedItemView"][f"{key}"]["price"]["price_USD"]
                except Exception as e:
                    print(f"{product_url} does not have {e}")

            if not json_data["props"]["pageProps"]["initialState"]["product"][
                "composedItemView"
            ][f"{prod_ids[0]}"]["isGrainFree"]:
                item["Grain_Free"] = "No"
            else:
                item["Grain_Free"] = "Yes"
            item["Life_Stage"] = json_data["props"]["pageProps"]["initialState"][
                "product"
            ]["composedItemView"][f"{prod_ids[0]}"]["details"]["table"][1]["text"]
            item["URL"] = product_url
            item["Rating"] = json_data["props"]["pageProps"]["initialState"]["product"][
                "seo"
            ]["structuredData"][1]["aggregateRating"]["ratingValue"]
            item["Reviews"] = json_data["props"]["pageProps"]["initialState"][
                "product"
            ]["seo"]["structuredData"][1]["aggregateRating"]["ratingCount"]
        self.results.append(item)

    def to_csv(self):
        with open("petco.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "petco.csv"')

    def run(self):
        base_url = "https://www.petco.com/shop/ProductListingView"
        product_urls = self.fetch_product_urls(base_url)

        for url in product_urls:
            self.parse_product_details(url)

        self.to_csv()


if __name__ == "__main__":
    scraper = PetCo()
    scraper.run()
    read_file = pd.read_csv("petco.csv").fillna("N\A")
    read_file.to_excel("petco.xlsx", index=None, header=True)
