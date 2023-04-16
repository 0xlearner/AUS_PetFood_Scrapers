import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import re
import traceback


class PetBarnProdScraper:

    all_info = []

    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url)
        print(f" | Status Code: {res.status_code}")

        return res

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        #!# [below] can be outside loop - doesn't change inside loop
        data = (
            soup.select_one(
                "script:-soup-contains('Overdose_AdobeAnalytics/js/default/ajaxComplete')"
            )
            .text.replace("\n", "")
            .strip()
        )
        data_json = json.loads(data)
        data_j = json.loads(
            data_json["*"]["Overdose_AdobeAnalytics/js/default/ajaxComplete"][
                "datalayer"
            ][0]
        )
        #!# [above] can be outside loop - doesn't change inside loop

        prodConts = soup.select('div.product-item-info[id^="product-id-"]')
        prodsJ = data_j["PLP"]["products"]

        for prodCont, prodJ in zip(prodConts, prodsJ):
            #!# [below] moved inside loop
            prod_id = prodCont.get("id").split("-")[-1]

            prodLink = prodCont.select_one("a.product-item-link")
            if prodLink:
                product_url = prodLink.get("href")
                title = " ".join(  #!# reduce whitescpace
                    [w for w in prodLink.text.split() if w]
                )
            else:
                product_url = title = "N/A"

            old_price = prodCont.select_one("span.old-price")
            last_price = (
                " ".join(  #!# reduce whitescpace
                    [w for w in old_price.text.split() if w]
                )
                if old_price
                else "N/A"
            )
            ratings = prodCont.select_one("div.rating-result[title]")
            ratings_count = ratings.get("title") if ratings else "N/A"
            no_of_reviews = prodCont.select_one("a.action.view")
            reviews_count = (
                " ".join(  #!# reduce whitescpace
                    [w for w in no_of_reviews.text.split() if w]
                )
                if no_of_reviews
                else "N/A"
            )
            #!# [above]  moved inside loop

            # for idx in range(len(titles)): #!# loops merged
            # try: ... # except... #!# no longer needed, already fixed above
            d = {
                "product_id": prod_id,  #!# added just bc
                "product_name": title,  # titles[idx], #!# loops merged
                "Regular_Price": prodJ["productPrice"],  #!# lists zipped
                "ratings": ratings_count,  #!# loops merged
                "number_of_reviews": reviews_count,  #!# loops merged
                "productSKU": prodJ["productSKU"],  #!# lists zipped
                "productSize": prodJ["productSize"],  #!# lists zipped
                "priceWithoutTax": prodJ["productPriceLessTax"],  #!# lists zipped
                "lifeStage": prodJ["lifeStage"],  #!# lists zipped
            }

            # self.all_info.append(d)

            #!# [below] unlooped
            try:
                details = soup.select_one(
                    f"script:-soup-contains('[data-role=swatch-option-{prod_id}]')"
                ).find_next()
                if details:
                    json_details = json.loads(details.text.replace("\n", "").strip())
                    dataJC = json_details[f"[data-role=swatch-option-{prod_id}]"][
                        "Magento_Swatches/js/swatch-renderer"
                    ]["jsonConfig"]
                    productId = dataJC["productId"]
                    jcInfs = [
                        {
                            "productId": productId,
                            "optionKey": k,
                            "sku": "?",
                            "index": v["1299"] if "1299" in v else None,
                        }
                        for k, v in dataJC["index"].items()
                    ]
                    orInfs = [
                        ("optionPrices", "amount", "reverseNest"),
                        ("dynamic", "value", "nest1"),
                        ("labels", "", "reverseNest"),
                        ("hasEndDate", "", "noNesting"),
                    ]

                    relevInfs = []
                    for kk, vk, nt in orInfs:
                        if kk not in dataJC:
                            continue
                        if nt == "noNesting":
                            relevInfs += [(kk, vk, dataJC[kk])]
                            continue
                        if nt == "nest1":
                            relevInfs += [(kk, vk, vd) for kk, vd in dataJC[kk].items()]
                            continue
                        if nt != "reverseNest":
                            ## can put a default action here
                            continue
                        ## nt == 'reverseNest'
                        orInf = {}
                        for pk, po in dataJC[kk].items():
                            # if isinstance(po, list):
                            #     continue
                            for kpo, vpo in po.items():
                                if kpo not in orInf:
                                    orInf[kpo] = {}
                                orInf[kpo][pk] = vpo

                        relevInfs += [(kk, vk, vi) for kk, vi in orInf.items()]
                        # print(relevInfs)

                    for i, j in enumerate(jcInfs):
                        for kk, vk, vd in relevInfs:
                            if j["optionKey"] not in vd:
                                continue
                            relevInf = vd[j["optionKey"]]
                            if type(relevInf) != dict:
                                j[kk] = relevInf
                            elif vk in relevInf and relevInf[vk]:
                                j[kk] = relevInf[vk]
                        # combine with main variation
                        jcInfs[i] = {
                            k: v
                            for k, v in (
                                list(d.items())
                                + [(jk, jv) for jk, jv in j.items() if jk not in d]
                            )
                        }
                    for j in jcInfs:
                        price_soup = BeautifulSoup(j["rendered_price"], "lxml")
                        member_price_html = price_soup.select_one(
                            "div.product-item-member-price__configural"
                        )
                        if member_price_html:
                            mph = price_soup.select_one("div.member-price").text
                            member_raw_price = [
                                p
                                for p in re.sub("<[^<]+?>", "", mph)
                                .replace("\n", "")
                                .split(" ")
                                if p
                            ]
                            print(member_raw_price)
                            j["Member_Price"] = member_raw_price[0]
                            rph = price_soup.select_one("div.regular-price").text
                            regular_price_html = [
                                p
                                for p in re.sub("<[^<]+?>", "", rph)
                                .replace("\n", "")
                                .split(" ")
                                if p
                            ]
                            print(regular_price_html)
                            j["Regular_Price"] = regular_price_html[-1]
                            self.all_info.append(j)

            except Exception as e:
                print(traceback.format_exc())
                self.all_info.append(d)

    def to_csv(self):

        df = pd.DataFrame(self.all_info).fillna("")

        #!# if you want to push some columns to the left
        firstCols = [  #!# adjust as you like
            "Scraped_Date",
            "Scraped_Time",
            "product_id",
            "productSKU",
            "sku",
            "product_name",
            "Member_Price",
            "Regular_Price",
            "ratings",
            "number_of_reviews",
        ]  #!# adjust as you like
        lfc = len(firstCols)
        oldCols = [
            (firstCols.index(c) if c in firstCols else lfc, i, c)
            for i, c in enumerate(list(df.columns.values))
        ]
        newCols = [oc[2] for oc in sorted(oldCols, key=lambda l: (l[0], l[1]))]
        df = df[newCols]
        final_df = df.drop(
            [
                "rendered_price",
                "oldPrice",
                "priceWithoutTax",
                "productId",
                "index",
                "baseOldPrice",
                "basePrice",
                "finalPrice",
                "tierPrices",
                "productSize",
            ],
            axis=1,
            errors="ignore",
        )
        #!# remove the above if you don't want to re-order columns

        csv_file = "petbarn_v2.csv"
        if not os.path.isfile(csv_file):
            final_df.to_csv(csv_file, index=False)
        else:
            final_df.to_csv(
                csv_file, mode="a", encoding="utf-8", header=False, index=False
            )

        print(f'Stored results to "petbarn_v2.csv"')  #!# just

    def run(self):
        for i in range(1, 2):  # total_number of pages
            url = f"https://www.petbarn.com.au/dogs/dog-treats?p={i}"
            # url = f"https://www.petbarn.com.au/dogs/dog-food/raw-fresh-frozen?p={i}"
            # url = f"https://www.petbarn.com.au/dogs/brand/prime100?p={i}"
            # url = f"https://www.petbarn.com.au/dogs/dog-food/dry-dog-food?p={i}"

            response = self.fetch(url)

            self.parse(response)
        self.to_csv()


if __name__ == "__main__":
    scraper = PetBarnProdScraper()
    scraper.run()
