https://www.petsmart.com/dog/food/fresh-food/freshpet/?pmin=0.01&srule=best-sellers&format=ajax

Reviews
start = response.text.index('{')
end = response.text.rfind(')')
data = json.loads(response.text[start:end])




https://www.petco.com/shop/en/petcostore/brand/freshpet

data = re.search(r"__NEXT_DATA__(.*)", response.text).group(1).replace('" type="application/json">', '')
json_data = json.loads(data[:data.index('</script>')])
prod_ids = list(json_data['props']['pageProps']['initialState']['product']['composedItemView'].keys())
for key in prod_ids:
    variants.append({json_data['props']['pageProps']['initialState']['product']['composedItemView'][f'{key}']['details']['table'][5]['text']: json_data['props']['pageProps']['initialState']['product']['composedItemView'][f'{key}']['price']['price_USD']})


https://www.amazon.com/s?k=Freshpet&i=pets&bbn=2619533011&rh=n%3A2619533011%2Cp_89%3AFreshpet&dc&qid=1673677058&refresh=1&rnid=2528832011&ref=sr_nr_p_89_1&ds=v1%3AA5QxOMCaCGDBacd0utOqlg8XrdUjfAbzv4UAdZKfQbQ



https://www.petstock.com.au/collections/prime?page=1&resultsPerPage=16&view=products

for product in products:
            try:
                images = product["images"]
            except KeyError:
                images = "N/A"
            d = {
                "Scraped_Date": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[0],
                "Scraped_Time": now.strftime("%m/%d/%Y, %H:%M:%S").split(",")[1],
                "brand": product["brand"],
                "prodcut_name": product["name"],
                "handle": product["handle"],
            }

headers = {
    'authority': 'api.searchspring.net',
    'accept': '*/*',
    'accept-language': 'en,ru;q=0.9',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36',
}

listing_params = {
    'siteId': 'hgffl8',
    'resultsFormat': 'native',
    'bgfilter.collection_id': '185088311432',
    'page': '1',
    'resultsPerPage': '16',
}

params = {
    'siteId': 'hgffl8',
    'resultsFormat': 'native',
    'page': '2',
    'resultsPerPage': '16',
    'q': 'prime',
}
json_blob = response.json()
handles = [handle['handle'] for handle in json_blob['results']]
total_pages = json_blob['pagination']['totalPages']
variants = [json.loads(variant['variants'].replace('\\&quot;', '').replace('&quot;', '"')) for variant in json_blob['results']]

product = [{'handle': d['handle']} for d in json_blob['results']]
for idx, var in enumerate(variants):
    product[idx]['var_size'] = [v['option1'] for v in var]
    product[idx]['price'] = [v['price'] for v in var]
    product[idx]['sku'] = [v['sku'] for v in var]
    product[idx]['barcode'] = [v['barcode'] for v in var]

https://www.petbarn.com.au/dogs/brand/prime100
[link.get('href') for link in soup.select('a.product-item-link')]

data = soup.select('script[type="application/ld+json"]')[0].string
json_blob = json.loads(data)
main_entity = json_blob[0]['mainEntity']['itemListElement']
product_urls = []
for url in main_entity:
    if 'url' in url['offers']:
        product_urls.append(url['url'])
    if 'offers' in url['offers']:
        urls = url['offers']['offers']
        for u in urls:
            product_urls.append(u['url])

product = []
pdpProductData = re.search(r"window.pdpProductData = (.*)", response.text).group(1)
clean_pd = re.sub('<[^<]+?>', '', pdpProductData).replace(';', '')
prod_data = json.loads(clean_pd)
if 'children' in prod_data:
    for k in prod_data['children'].keys():
        product.append([{'product_id': prod_data['children'][key]['id'], 'product_sku': prod_data['children'][key]['sku'], 'product_name': prod_data['children'][key]['name']} for key in prod_data['children'].keys()])
else:
    product.append[{'product_id': prod_data['sku'], 'product_sku': prod_data['id'], 'product_name': prod_data['name']}]

html_json = re.search(r"window.odProductConfig = (.*)", response.text).group(1)
json_str = re.sub('<[^<]+?>', '', html_json).replace(';', '')
json_blob = json.loads(json_str)
for idx, prod_id in enumerate(product):
    main_entity = json_blob['products'][prod_id['product_id']]
    if 'regular_price' in main_entity:
        product[idx]['regular_price'] = main_entity['regular_price']
    if 'member_price' in main_entity:
        product[idx]['member_price'] = main_entity['member_price']
    if 'save_amount' in main_entity:
        product[idx]['save_amount'] = main_entity['save_amount']


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


https://www.petcircle.com.au/prime100



https://freshpet.com/where-to-buy/#/




if "children" in prod_data:
            prodID = list(prod_data["children"].keys())
            product_dict["product_id"] = {
                prodID[idx]: prod_data["children"][key]["id"]
                for idx, key in enumerate(prod_data["children"].keys())
            }
            product_dict["product_sku"] = {
                prodID[idx]: prod_data["children"][key]["sku"]
                for idx, key in enumerate(prod_data["children"].keys())
            }
            product_dict["product_name"] = {
                prodID[idx]: prod_data["children"][key]["name"]
                for idx, key in enumerate(prod_data["children"].keys())
            }

        if "children" not in prod_data:
            product_dict["product_id"] = prod_data["id"]
            product_dict["product_sku"] = prod_data["sku"]
            product_dict["product_name"] = prod_data["name"]
        # product.append(d)
        # self.all_info.append(product_dict)
        # print(product_dict)
        html_json = re.search(r"window.odProductConfig = (.*)", response.text).group(1)
        json_str = re.sub("<[^<]+?>", "", html_json).replace(";", "")
        json_blob = json.loads(json_str)
        for element in list(product_dict.values()):
            if not isinstance(element, dict):
                k = product_dict["product_id"]
                # print(k)
            else:
                for i in list(element.keys()):
                    k = product_dict["product_id"][i]
            main_entity = json_blob["products"][k]
            # print(main_entity)
            if "regular_price" in main_entity:
                product_dict["regular_price"] = main_entity["regular_price"]
            if "member_price" in main_entity:
                product_dict["member_price"] = main_entity["member_price"]
            if "save_amount" in main_entity:
                product_dict["save_amount"] = main_entity["save_amount"]


https://www.petco.com/shop/en/petcostore/category/dog/dog-food/dry-dog-food?params=page2

url = 'https://ac.cnstrc.com/browse/group_id/dry-dog-food'
response = httpx.get(url, params=params, headers=headers)
product_urls = ["https://www.petco.com" + u['data']['url'] for u in response.json()['response']['results']]

import requests
import re
import json
import html

headers = {
    'authority': 'www.budgetpetproducts.com.au',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en,ru;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_ALGOLIA=anonymous-6d2b7032-518b-4da0-b0b9-964e00920f3d; scarab.visitor=%2245DBAC5A87F9C262%22; _fbp=fb.2.1674782859328.577366252; _tt_enable_cookie=1; _ttp=jTkn1Rm860eDgPiXlG45pfHRDG7; _gid=GA1.3.415748101.1675529773; _ga=GA1.3.583864494.1674782855; _uetsid=d505d7e0a4ac11ed962a7de239a71ea1; _uetvid=c75d7e109de111eda4efb3023338d7ad; XSRF-TOKEN=eyJpdiI6IkJjNVpiMzNQRGFRYzJ6Z1ZUR2NEVFE9PSIsInZhbHVlIjoiSGNyN2J4dUtza1JadUhqUFAwWklWcFdIVmZLSC84OEp4TUtRYWdLQzBhUU1GK2psMzFHQW5SVTlZZm1Yd0xmaGt3QWFoRDVsNVYyRGdKYVRKbUZSak9UMzlCZEhXc0FubjdORERraE5nRHNsYWViVkxZZCt6d2VkbGNGNjhNWlciLCJtYWMiOiIyZjQxMzk5YjZjZWNmM2E1MmVjYmQxODAxNDY3ZWY1MTZiM2MyNzcwODBmY2ZlNWM5YTVmMDU4MWMwMDViZjQ5In0%3D; budget_pet_products_session=eyJpdiI6IkdnVHVrTjlkUGY1SGxMN0lZWTVsckE9PSIsInZhbHVlIjoibERhNnllekN5azRhMEptSU9QeGZ3VkVaYUpsUkxGbi9rR21yMXArWEoycWdlMWJSZFRnL3BtOUhBMXBXQ0syVEJPbUtaOVVpLzRkdFBwRDZsUU45V3lxd1JzK2lTU1RyLzkyM24xcTR2TUUvQVdrdEV0VHpoRDFIVFNBZHJTVTgiLCJtYWMiOiIwNDAzMTM3YmQ5YWE3ZWY3NmE3MjA3OGEyMTZmMWM5ODY3ZjlkOGZjNDEyYzkzNmM5MzhjY2ZkODcyNmU3N2NjIn0%3D; scarab.profile=%221677%7C1675608432%7C8787%7C1675608372%7C3624%7C1675146623%22; _ga_6YGE1ZKCTV=GS1.1.1675608368.2.1.1675608533.0.0.0',
    'referer': 'https://www.budgetpetproducts.com.au/dog/food?sort=best_match',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36',
}

response = requests.get(
    'https://www.budgetpetproducts.com.au/product/royal-canin-maxi-adult-dry-dog-food-4kg/1679',
    headers=headers,
    )

data = re.search(':data=(.*)', response.text).group(1).replace(':is-mobile="false"></product-page-component>', '').replace('&quot;', '"').replace('\\"', '').replace('/', '').replace("\'", "'").strip()
clean_data = html.unescape(data)


from selectolax.parser import HTMLParser

html = HTMLParser(response.text)

urls = ["https://www.mypetwarehouse.com.au" + link.attributes['href'] for link in html.css('a.list-item-link')]
mylist = list(dict.fromkeys(urls))

product_url = html.css_first('meta[property="og:url"]').attributes['content']
product_id = product_url.split('-')[-1]
product_name = html.css_first('h1.p-product-title_.h3_.theme-font_.mt5').text().strip()
sku = html.css_first('[itemprop="sku"]').text()
upc = html.css_first('[itemprop="gtin"]').text()
brand = html.css_first('meta[property="og:brand"]').attributes['content']
price = html.css_first('span.text-price').text()
rating = html.css_first('[itemprop="ratingValue"]').text()
reviews = html.css_first('[itemprop="reviewCount"]').text()
availability = html.css_first('[itemprop="availability"]').text()

cat = ["dog-food", "dog-treats"]
data = f"""{{"requests":[{{"indexName":"shopify_pc1_products","params":"clickAnalytics=true&facetFilters=%5B%5B%22collections%3A{cat}%22%5D%5D&facets=%5B%22collections%22%2C%22grams%22%2C%22tags%22%2C%22collection_ids%22%2C%22vendor%22%2C%22named_tags.categories%22%2C%22price%22%2C%22named_tags.breed%20size%22%2C%22named_tags.benefits%22%2C%22named_tags.lifestyle%22%2C%22named_tags.life%20stage%22%2C%22inventory_available%22%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=16&maxValuesPerFacet=50&page=1&query=&tagFilters="}},{{"indexName":"shopify_pc1_products","params":"analytics=false&clickAnalytics=false&facets=collections&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=50&page=0&query="}}]}}"""
response = httpx.post('https://cq45c0coif-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.11.3)%3B%20react%20(18.2.0)%3B%20react-instantsearch%20(6.38.3)&x-algolia-api-key=30f78909ba0ca139096a649889583a26&x-algolia-application-id=CQ45C0COIF', headers=headers, data=data)

products = response.json()['results'][0]['hits']
product_urls = ['https://www.petculture.com.au/_next/data/JHtsvxybFyzeiLoEUTCda/products/' + url['handle']+'-'+url['sku']+'.json' for url in products]



datalayer = re.search( r"window.adobeDatalayerEvents = (.*)", response.text).group(1).replace(';', '')
products = json.loads(datalayer)
product_list = json.loads(products[0])['PLP']['products']
breadcrumb = json.loads(products[0])['PLP']['productBreadcrumbs']
product_skus = [sku['productSKU'] for sku in product_list]
product_data = [{'product_sku': pd['productSKU'], 'product_name': pd['productName'], 'life_stage': pd['lifeStage'], 'category': '-'.join(breadcrumb.split('-')[1:])} for pd in product_list]
# json_data = {
#     "query": f"""query {{ products (filter: {{ sku: {{ in: "{product_skus}"}}}}) {{    items {{      id sku thumbnail {{ url label }} member_price ...on ConfigurableProduct {{ variants {{ attributes {{ uid label code }} product {{ id sku  thumbnail {{ url label }} member_price price_range {{ minimum_price {{ final_price {{value}} regular_price {{value}} }} }} }} }} }} price_range {{ minimum_price {{ final_price {{value}} regular_price {{value}} }} }} }} }} }}""",
# }

# import requests

# headers = {
#     "authority": "www.petbarn.com.au",
#     "accept": "*/*",
#     "accept-language": "en,ru;q=0.9",
#     "content-type": "application/json",
#     "cookie": "form_key=H4T0fcvSEeqWdLtR; PHPSESSID=c1514aa75719bd4bccae91b4bd378715; _hjSessionUser_697727=eyJpZCI6ImMxZTQzZDE0LWJiMDAtNThlNi05YThhLTFlODcxMWQ3NWQwNSIsImNyZWF0ZWQiOjE2NjgyNjY5MDAyNTMsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.1814422308.1673680421; s_ecid=MCMID%7C14352294586015616793216407977341736282; aam_uuid=19481282441348406572612417380699116100; _fbp=fb.2.1673680424775.13195942; mage-messages=; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; mage-cache-sessid=true; product-selected-swatch-options=%7B%7D; changeYoutubeCode=; at_check=true; AMCVS_CAFC1FE55D6CC83E0A495E73%40AdobeOrg=1; s_vnc365=1707513620074%26vn%3D9; s_ivc=true; s_inv=1776064; _gid=GA1.3.1119137798.1675977621; s_cc=true; _hjSession_697727=eyJpZCI6IjFkMjFmZmIwLTAzMGQtNGFlYi1hMzQ5LThmMmZjZjg3NTA0ZCIsImNyZWF0ZWQiOjE2NzU5Nzc2MjgwODgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _pin_unauth=dWlkPU16Y3dNbVF6T0dNdE1tWTBOaTAwWTJSa0xUazVZakV0TXprek5XWm1ZV014WWprMw; _hjIncludedInSessionSample=0; AMCV_CAFC1FE55D6CC83E0A495E73%40AdobeOrg=-1124106680%7CMCIDTS%7C19398%7CMCMID%7C14352294586015616793216407977341736282%7CMCAID%7CNONE%7CMCOPTOUT-1675992719s%7CNONE%7CMCAAMLH-1676590319%7C3%7CMCAAMB-1676590319%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-19405%7CvVersion%7C5.2.0; section_data_ids=%7B%22live_chat%22%3A1675986741%2C%22autocomplete-address%22%3A1675986745%2C%22pickup-store%22%3A1675986748%2C%22launch%22%3A1675986748%7D; catURL=https%3A%2F%2Fwww.petbarn.com.au%2Fdogs%2Fdog-food%2Fdry-dog-food; _derived_epik=dj0yJnU9c0pidkJnZzdob1VzOFEycldUUnBiT1FHLW1iZjVLcHombj02dDZLa1I5N0F1aDI2czJkaUpOeG9RJm09MSZ0PUFBQUFBR1BsaUFZJnJtPTEmcnQ9QUFBQUFHUGxpQVkmc3A9Mg; _uetsid=95fc0d10a8bf11ed9956e72a409094f1; _uetvid=aa29f960629e11edafaa2973a52bbfa2; private_content_version=9b8bcf27337fd89d38dfd8f773483c99; catURL=https%3A%2F%2Fwww.petbarn.com.au%2Fdogs%2Fdog-food%2Fdry-dog-food%3Fp%3D2%26product_list_order%3Dposition; s_sq=%5B%5BB%5D%5D; BE_CLA3=p_id%3DLAR2J2448244RJ2NP22N4J6N8AAAAAAAAH%26bn%3D22%26bv%3D3.45%26s_expire%3D1676073768401%26s_id%3DLAR2J2448244R2N8JJ8N4J6N8AAAAAAAAH; gpv_Page=petbarn%3Aadvance-total-wellbeing-chicken-all-breed-adult-dog-food; s_nr30=1675987368480-Repeat; s_tslv=1675987368499; _gat_UA-27528868-1=1; _ga_BW9RWVMF8W=GS1.1.1675977621.11.1.1675987369.60.0.0; mbox=PC#613a8353cdab419e8249b9f573c8eae8.38_0#1739232171|session#fd9c3f2c35514e3898ee874bb568b170#1675989231; _ga=GA1.3.298394843.1673680423",
#     "origin": "https://www.petbarn.com.au",
#     "referer": "https://www.petbarn.com.au/advance-total-wellbeing-chicken-all-breed-adult-dog-food?sku=25196",
#     "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Yandex";v="23"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Linux"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1038 (beta) Yowser/2.5 Safari/537.36",
#     "x-newrelic-id": "VgMAVlRWCRAEVllTDwQBV1E=",
#     "x-requested-with": "XMLHttpRequest",
# }

# json_data = {
#     "query": 'query { products (filter: { sku: { in: ["advance-medium-breed-lamb-&-rice-adult-dog-food","advance-medium-breed-chicken-&-rice-puppy-dog-food","advance-medium-breed-chicken-&-rice-adult-dog-food","advance-large-breed-chicken-&-rice-puppy-dog-food","eukanuba-adult-dog-food","advance-medium-breed-chicken-&-rice-puppy-dog-food","advance-sm-breed-hlthy-weight-chk-rice-adult-dog-food","probalance-total-health-chicken-dog-food","136467","probalance-total-health-salmon-dog-food","122389","139363","advance-small-breed-chicken-adult-dog-food","136459","eukanuba-mature-&-senior-dog-food","billy-&-margot-lamb-superfood-adult-dog-food","advance-med-breed-hlthy-weight-chk-rice-adult-dog-food","royal-canin-dachshund-adult-dog-food","science-diet-perfect-weight-adult-dog-food","probalance-care-joint-care-adult-dog-food","advance-mobility-large-adult-dog-food","savourlife-grain-free-sensitive-ofish-adult-dog-food","ivory-coat-grain-free-reduced-fat-turk-senior-dog-food","science-diet-small-sensitive-stm-&-skn-adlt-dog-food","royal-canin-maxi-breed-puppy-food","advance-small-breed-lamb-&-rice-adult-dog-food","black-hawk-grain-free-chicken-adult-dog-food","98510","advance-medium-breed-chicken-&-rice-puppy-dog-food","black-hawk-grain-free-salmon-adult-dog-food","advance-med-breed-hlthy-weight-chk-rice-adult-dog-food","advance-lg-breed-hlthy-ageing-chck-rice-adult-dog-food","hills-presc-diet-gastro-biome-adult-dog-food","136466","advance-small-breed-chicken-&-rice-puppy-dog-food","advance-medium-breed-lamb-&-rice-adult-dog-food","ivory-coat-grain-free-ocean-fish-&-salm-adult-dog-food","royal-canin-medium-breed-adult-dog-food","royal-canin-maxi-breed-puppy-food","royal-canin-poodle-adult-dog-food"]}}) {    items {      id sku thumbnail { url label } member_price ...on ConfigurableProduct { variants { attributes { uid label code } product { id sku  thumbnail { url label } member_price price_range { minimum_price { final_price {value} regular_price {value} } } } } } price_range { minimum_price { final_price {value} regular_price {value} } } } } }',
# }

# response = requests.post(
#     "https://www.petbarn.com.au/graphql", headers=headers, json=json_data
# )


soup = BeautifulSoup(response.text, "html.parser")
        next_page = soup.select_one("li.item.pages-item-next > a").get("href")
        if next_page is not None:
            print(f"Fetching {next_page}")
            self.fetch_base_url(next_page)