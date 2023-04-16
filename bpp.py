import requests
import re
import json
import html

headers = {
    "authority": "www.budgetpetproducts.com.au",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en,ru;q=0.9",
    "cache-control": "max-age=0",
    # 'cookie': '_ALGOLIA=anonymous-6d2b7032-518b-4da0-b0b9-964e00920f3d; scarab.visitor=%2245DBAC5A87F9C262%22; _fbp=fb.2.1674782859328.577366252; _tt_enable_cookie=1; _ttp=jTkn1Rm860eDgPiXlG45pfHRDG7; _gid=GA1.3.415748101.1675529773; _ga=GA1.3.583864494.1674782855; _uetsid=d505d7e0a4ac11ed962a7de239a71ea1; _uetvid=c75d7e109de111eda4efb3023338d7ad; XSRF-TOKEN=eyJpdiI6IkJjNVpiMzNQRGFRYzJ6Z1ZUR2NEVFE9PSIsInZhbHVlIjoiSGNyN2J4dUtza1JadUhqUFAwWklWcFdIVmZLSC84OEp4TUtRYWdLQzBhUU1GK2psMzFHQW5SVTlZZm1Yd0xmaGt3QWFoRDVsNVYyRGdKYVRKbUZSak9UMzlCZEhXc0FubjdORERraE5nRHNsYWViVkxZZCt6d2VkbGNGNjhNWlciLCJtYWMiOiIyZjQxMzk5YjZjZWNmM2E1MmVjYmQxODAxNDY3ZWY1MTZiM2MyNzcwODBmY2ZlNWM5YTVmMDU4MWMwMDViZjQ5In0%3D; budget_pet_products_session=eyJpdiI6IkdnVHVrTjlkUGY1SGxMN0lZWTVsckE9PSIsInZhbHVlIjoibERhNnllekN5azRhMEptSU9QeGZ3VkVaYUpsUkxGbi9rR21yMXArWEoycWdlMWJSZFRnL3BtOUhBMXBXQ0syVEJPbUtaOVVpLzRkdFBwRDZsUU45V3lxd1JzK2lTU1RyLzkyM24xcTR2TUUvQVdrdEV0VHpoRDFIVFNBZHJTVTgiLCJtYWMiOiIwNDAzMTM3YmQ5YWE3ZWY3NmE3MjA3OGEyMTZmMWM5ODY3ZjlkOGZjNDEyYzkzNmM5MzhjY2ZkODcyNmU3N2NjIn0%3D; scarab.profile=%221677%7C1675608432%7C8787%7C1675608372%7C3624%7C1675146623%22; _ga_6YGE1ZKCTV=GS1.1.1675608368.2.1.1675608533.0.0.0',
    "referer": "https://www.budgetpetproducts.com.au/dog/food?sort=best_match",
    "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
}

response = requests.get(
    "https://www.budgetpetproducts.com.au/product/royal-canin-maxi-adult-dry-dog-food-4kg/1679",
    # "https://www.budgetpetproducts.com.au/product/royal-canin-dachshund-adult-loaf-pouches-wet-dog-food-12-x-85g/10450",
    headers=headers,
)

data = (
    re.search(":data=(.*)", response.text)
    .group(1)
    .replace(':is-mobile="false"></product-page-component>', "")
    .replace("&quot;", '"')
    .replace("'", '\\"')
)


def striphtml(data):
    p = re.compile(r"<.*?>")
    return p.sub("", data)


clean_data = html.unescape(data)
json_blob = json.loads(clean_data[1:-2])
product = json_blob["variances"][0]["options"]
desc = json_blob["descriptions"]
for d in desc:
    if "Feeding Guide" in d["type"]:
        print(striphtml(d["description"]).replace("\n", "").replace("&nbsp;", ""))
