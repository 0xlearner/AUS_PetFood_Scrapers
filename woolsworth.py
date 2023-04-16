import httpx
from http.cookies import SimpleCookie
from playwright.sync_api import sync_playwright
import pandas as pd
import math
import re
from datetime import datetime
from datetime import date

now = datetime.now()
today = date.today()

TAG_RE = re.compile(r"<[^>]+>")


def remove_tags(text):
    return TAG_RE.sub(" ", text)


# def get_site_cookies(url: str) -> dict:
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url)
#         cookies_list = page.context.cookies()
#         cookies_dict = {el["name"]: el["value"] for el in cookies_list}
#         browser.close()

#     return cookies_dict


# cookies = get_site_cookies(initial_url)


class WoolsWorthScraper:

    all_info = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        # 'Accept-Encoding': 'gzip, deflate, br',
        "Content-Type": "application/json",
        "Request-Id": "|ff65d6a2b5ef40deba161436fc928041.6fdc6ae6448243a2",
        "Request-Context": "appId=cid-v1:4601595d-64c0-46e0-be60-45622438acb3",
        "traceparent": "00-ff65d6a2b5ef40deba161436fc928041-6fdc6ae6448243a2-01",
        "Origin": "https://www.woolworths.com.au",
        "Connection": "keep-alive",
        "Referer": "https://www.woolworths.com.au/shop/browse/pet/dog-puppy?pageNumber=2",
        # "Cookie": "_abck=1AF9FA9968986E01D95DE635CE5CA49A~0~YAAQxKwwF9AxTzCGAQAAxiD3bAmsSwB2l0fu0Qkxwjxnj0eBYY2KO8HjhItiu5sN7xFgjkvdQqKgyv/hu4VkBsWJ3oYiyNXI14J3VvZGyn8YlAXhwkpxUFARbsS77w/DPoYunsl9ebanNTa5tkHlGnljdRYEP3t/wbKcd/nsI4HMtUFPK6ue8otsWnYwo1Bh36es48ACGX36BGjeA499YjAIltTnyPWNVRWm6QtaGoxoU2mixG6z2Z5Lk+GoizGD7EwOeYR5kXJTFSC+OhfiQmGOLafeGxFYrrw7yqiy2PCRQlcq2/uTk1LSaTFkBifkg8UVXHraNU6s0gZbtDRhaix8+ioePm0gsd3IQDsFM5HwLS2AtyLaT9B+QdlydT50nft3XKx2gOXXBTXqEiXdRCVTLrrlpVXzvoMuPvRNaA==~-1~-1~-1; AMCV_4353388057AC8D357F000101%40AdobeOrg=870038026%7CMCIDTS%7C19408%7CMCMID%7C39487458205068416855238848785487881282%7CMCOPTOUT-1676872577s%7CNONE%7CvVersion%7C5.0.0; ai_user=fL4KLTsKGOkSYGQVYJwdIm|2023-02-17T10:51:04.008Z; utag_main=v_id:01865effc7310001995bec5e16700504600370090086e; AKA_A2=A; akaalb_woolworths.com.au=~op=www_woolworths_com_au_BFF_MEL:WOW-BFF-MEL|www_woolworths_com_au_ZoneB:PROD-ZoneB|www_woolworths_com_au_BFF_MEL_Launch:WOW-BFF-MEL|~rv=38~m=PROD-ZoneB:0|WOW-BFF-MEL:0|~os=43eb3391333cc20efbd7f812851447e6~id=994ae2ad8d40ae4f894208c8efa8f90b; ak_bmsc=66320F9DDA68208B9C0D55A35DCB1E9C~000000000000000000000000000000~YAAQxKwwF8kxTzCGAQAAjRz3bBJVwgNzhzJMpljtUkZOOQeE+27f7XbTT9ERG1i7v88IxKavwFLbIeq3sYSIvpgsMxN5oS/ZpPGz46kuEEHSI1t6RSCSjBRJG1O0pxwlhXCKmwup688hxpv0aBM+fPfXSVbh5VJhenskXxcHHnyBQju3rFwLfPDzA0VuoEt9Nu5esXFBci+C+ZQ5TCCoUFoWqPi77a0hR43VmaoTnnPQHnxuUbQMN68MT0+HdgEEKDos8h887II1whD69+vIei9yDQFh/BJ8pLXSijwY7uJveNXS9iO/oUfzu3pSOhiFBssHijHtMwuAC1HG9OSPhAg/huTbTubMengbhfNa/q2+Q/JJnGo6Tiz84dltIYcnr6TVzVVdFwyRjQkr5TVa9RsMxhVzfFzpZP1mk0Ya5hAfjV9qzGIiO4EMi7HtD7yOqSL+z8wpgdB+OJPCSdWG83LV3l1frAKwgW2MccKQOmcBTSHE0UvazB6LGOJNhTqD3lqYNIsvcdvFTDjbbIHCoxT9tOo22A==; bm_sz=2BE74D2F94FD38AA4F1E55F6C1F9188D~YAAQxKwwF70xTzCGAQAA+RD3bBKyUXhOFZJhgV4xph4IyzASZFnO7x0YSadZ/ShjLYP8dZgY3quZjGYLMTExGlimRcHMNYN4vOrIet4GQrogX8VjrQO4w8a7oTGJAbEsRoblyp9rm/0f2fmYIfVHEKZ/zbAHMsNgwpXV+bavPMAT6HS6bk3AFWT1OFYwWQjqwWvXCI1PRTXrCTV0gwqZavteliAcnE2o+mLHvM+xmTIK4H0LAz4PREpgrutV4xdKJdPqjWDmza/0nkHbl8ZAYXjWJaxZwzhzhGiWBnoloK0eXQjJXWS030hm~4473668~4405558; dtCookie=v_4_srv_-2D56_sn_9E6PQ066TSE6586TQN5508G53GNOV6JD; rxVisitor=16768653768100HJM7JQLRTRONBMC8TQOR7A4LNIEL8GJ; dtPC=-56$465376777_250h1vVVUHQOATEPUJHRKQFCCCKRJPMTHKRECQ-0e0; rxvt=1676867176818|1676865376818; INGRESSCOOKIE=1676865377.813.45.481628|37206e05370eb151ee9f1b6a1c80a538; at_check=true; mbox=session#7f5b89582cf94c6f80497a78f463dff4#1676867240; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2NzY4NjUzNzcsImV4cCI6MTY3Njg2ODk3NywiaWF0IjoxNjc2ODY1Mzc3LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjI4ZTcwYjVlLTcxNDAtNGZhMy05Y2E2LTc2YzFlYWVjZTgxYiIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.UEK0YeJ96xgcYOkQUPhlpEssxXDujbZatvUKtFJ9HK7zn3IFeOxRfZ5pb5UOTsXH4-6FoEB5YK3fqJuF4Xq88C-0T_XiuClaUGL5fIU3E8iOxQYgfMBJT5pMlYqZ5v6mD2V9DIjfF8Np15nIbPdxW_imN7BXhI6Fa7RNI5xow3SkxMzpiDiD_SgHjfZKPq-ifcpZHKbUSotpXKjRlHCQC8MM1fwMX4v1FPepI8r0YM4_ZZCeidJsHpoZPqhqWq_n822s_Ubmoi-fAJ3nQa_pUR3O20HmwOhmVaUvkqDIahYugDbbmF7bDojDawU4YP8qm2uf_immjaS-FbkHU1k9mg; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2NzY4NjUzNzcsImV4cCI6MTY3Njg2ODk3NywiaWF0IjoxNjc2ODY1Mzc3LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjI4ZTcwYjVlLTcxNDAtNGZhMy05Y2E2LTc2YzFlYWVjZTgxYiIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.UEK0YeJ96xgcYOkQUPhlpEssxXDujbZatvUKtFJ9HK7zn3IFeOxRfZ5pb5UOTsXH4-6FoEB5YK3fqJuF4Xq88C-0T_XiuClaUGL5fIU3E8iOxQYgfMBJT5pMlYqZ5v6mD2V9DIjfF8Np15nIbPdxW_imN7BXhI6Fa7RNI5xow3SkxMzpiDiD_SgHjfZKPq-ifcpZHKbUSotpXKjRlHCQC8MM1fwMX4v1FPepI8r0YM4_ZZCeidJsHpoZPqhqWq_n822s_Ubmoi-fAJ3nQa_pUR3O20HmwOhmVaUvkqDIahYugDbbmF7bDojDawU4YP8qm2uf_immjaS-FbkHU1k9mg; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2NzY4NjUzNzcsImV4cCI6MTY3Njg2ODk3NywiaWF0IjoxNjc2ODY1Mzc3LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjI4ZTcwYjVlLTcxNDAtNGZhMy05Y2E2LTc2YzFlYWVjZTgxYiIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.UEK0YeJ96xgcYOkQUPhlpEssxXDujbZatvUKtFJ9HK7zn3IFeOxRfZ5pb5UOTsXH4-6FoEB5YK3fqJuF4Xq88C-0T_XiuClaUGL5fIU3E8iOxQYgfMBJT5pMlYqZ5v6mD2V9DIjfF8Np15nIbPdxW_imN7BXhI6Fa7RNI5xow3SkxMzpiDiD_SgHjfZKPq-ifcpZHKbUSotpXKjRlHCQC8MM1fwMX4v1FPepI8r0YM4_ZZCeidJsHpoZPqhqWq_n822s_Ubmoi-fAJ3nQa_pUR3O20HmwOhmVaUvkqDIahYugDbbmF7bDojDawU4YP8qm2uf_immjaS-FbkHU1k9mg; bm_sv=A384BB54394BFFBBF9277F772238C50F~YAAQxKwwFwsyTzCGAQAAWkX3bBJJoDs/gJ3TG6zMp3HVW2g4HQ5+8iD06O4UWV6ZYHK5Nd00Q20lrEutmUYcZSV07OuemApEpZ+25As+xUEhAUcoh1JCsrkjbsdBMUQdlBj5LNR0WaR76d4aLEAszXmBGDkrZmK98Q7OpYDMmfyaff8fw6u/qI9MBYUBAwuRFxR+xo1kX8gdKE0FiFYHGoyB2FA8iMP4MYzKGH/xegz+C7Ei271MNXB+crWZOORODApP0kDLhQ==~1; bm_mi=80BA8C6828A8644CDA09DB11ECB2499B~YAAQxKwwF8ExTzCGAQAA6hP3bBL0glag+IIL0mU0/EVmDU10GjOmkUqLhxwefohLPypRGAkN0BATviz0N8DW0x78quux78pOX1xFPZn5zf3ISMnxvgl6aBy6qjmcCrsgXtM6dIUmRruZm0ipb/Ef2e0v50SKsgiPlZEdbbPF7YK5Ywd8u6Hd+ER6p4dfwC+KfinYHfaAg7E60tN8l2YHlwAVI8CwoXoB5oN2Qkodt/dQRG6fX5CUVYd09x4CKF2CTi5PZr+8lBwPuNAgW+0tWU1hFspAbRgTpa84Z//zEZnqMPUAgxprfJUipIOtt7FfibG7TNLgmphBdctA6LV72JEY/RQb~1; AMCVS_4353388057AC8D357F000101%40AdobeOrg=1; ai_session=uEFiMV9iVA98/Qzf+BLd+R|1676865379549|1676865379549; fullstoryEnabled=false",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    dog_json_data = {
        "categoryId": "1_EF205FA",
        "pageNumber": 1,
        "pageSize": 36,
        "sortType": "TraderRelevance",
        "url": "/shop/browse/pet/dog-puppy?pageNumber=1",
        "location": "/shop/browse/pet/dog-puppy?pageNumber=1",
        "formatObject": '{"name":"Dog & Puppy"}',
        "isSpecial": False,
        "isBundle": False,
        "isMobile": True,
        "filters": [],
        "token": "",
        "enableGp": False,
        "isHideUnavailableProducts": False,
    }

    cat_json_data = {
        "categoryId": "1_1969229",
        "pageNumber": 2,
        "pageSize": 36,
        "sortType": "TraderRelevance",
        "url": "/shop/browse/pet/cat-kitten?pageNumber=2",
        "location": "/shop/browse/pet/cat-kitten?pageNumber=2",
        "formatObject": '{"name":"Cat & Kitten"}',
        "isSpecial": False,
        "isBundle": False,
        "isMobile": True,
        "filters": [],
        "token": "",
        "enableGp": False,
        "isHideUnavailableProducts": False,
    }

    list_json_data = [dog_json_data, cat_json_data]

    base_url = "https://www.woolworths.com.au/apis/ui/browse/category"

    initial_url = "https://www.woolworths.com.au/shop/browse/pet/dog-puppy"

    cookie = SimpleCookie()

    res = httpx.get(initial_url, headers=headers)
    c = res.cookies
    cookie.load(c)
    cookies = {key: value.value for key, value in cookie.items()}

    def return_json_data(self):
        for json_data in self.list_json_data:
            return json_data

    def fetch(self, url):
        print(f"HTTP POST request to URL: {url}", end="\n")
        with httpx.Client(headers=self.headers) as client:
            for json_data in self.list_json_data:
                resp = client.post(
                    self.base_url,
                    cookies=self.cookies,
                    json=json_data,
                    timeout=40,
                )
                print(f" | Status Code: {resp.status_code}")
                return resp

    def pagination(self, response):
        # cookies = self.get_site_cookies(self.initial_url)
        json_blob = response.json()
        products = json_blob["Bundles"]
        total_items = json_blob["TotalRecordCount"]
        total_pages = round(math.ceil(total_items / len(products)))
        for json_data in self.list_json_data:
            for page_no in range(1, total_pages + 1):
                json_data["pageNumber"] = page_no
                print(
                    f"HTTP POST request page {page_no}",
                    end="\n",
                )
                with httpx.Client(headers=self.headers) as client:
                    resp = client.post(
                        self.base_url,
                        cookies=self.cookies,
                        json=json_data,
                        timeout=40,
                    )
                    self.parse(resp)

    def parse(self, response):
        products = response.json()["Bundles"]
        for prod in products:
            item = {}
            product = prod["Products"][0]
            item["Scraped_Date"] = now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0]
            item["Scraped_Time"] = now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1]
            item["Stock_Code"] = product["Stockcode"]
            item["Product_Name"] = product["Name"]
            item["Product_Category"] = (
                product["AdditionalAttributes"]["piescategorynamesjson"]
                .strip("][")
                .strip('"')
            )
            item["Sub_Category"] = (
                product["AdditionalAttributes"]["piessubcategorynamesjson"]
                .strip("][")
                .strip('"')
            )
            item["Brand"] = product["Brand"]
            item["Price/100g"] = product["CupPrice"]
            item["Price"] = product["Price"]
            item["Was_Price"] = product["WasPrice"]
            item["Save"] = product["SavingsAmount"]
            item["Size"] = product["PackageSize"]
            try:
                item["Description"] = remove_tags(
                    product["AdditionalAttributes"]["description"]
                    .replace("\r", "")
                    .replace("\n", "")
                    .strip()
                )
            except:
                item["Description"] = "N/A"
            item["Ingredients"] = product["AdditionalAttributes"]["ingredients"]
            item["Availability"] = (
                "InStock" if product["IsAvailable"] else "Out of Stock"
            )
            item["Image"] = product["LargeImageFile"]

            self.all_info.append(item)

    def to_csv(self):
        df = pd.DataFrame(self.all_info).fillna("N/A")

        df.to_csv(f"woolsworth.csv", index=False)

        print('Stored results to "woolsworth.csv"')

    def run(self):

        init_response = self.fetch(self.base_url)

        self.pagination(init_response)
        self.to_csv()


if __name__ == "__main__":
    scraper = WoolsWorthScraper()
    scraper.run()
