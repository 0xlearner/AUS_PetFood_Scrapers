page = 5
cat = "dog-food"
data = f"""{{"requests":[{{"indexName":"shopify_pc1_products","params":"clickAnalytics=true&facetFilters=%5B%5B%22collections%3A{cat}%22%5D%5D&facets=%5B%22collections%22%2C%22grams%22%2C%22tags%22%2C%22collection_ids%22%2C%22vendor%22%2C%22named_tags.categories%22%2C%22price%22%2C%22named_tags.breed%20size%22%2C%22named_tags.benefits%22%2C%22named_tags.lifestyle%22%2C%22named_tags.life%20stage%22%2C%22inventory_available%22%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=16&maxValuesPerFacet=50&page={page}&query=&tagFilters="}},{{"indexName":"shopify_pc1_products","params":"analytics=false&clickAnalytics=false&facets=collections&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=50&page=0&query="}}]}}"""
print(
    f"""{{"requests":[{{"indexName":"shopify_pc1_products","params":"clickAnalytics=true&facetFilters=%5B%5B%22collections%3A{cat}%22%5D%5D&facets=%5B%22collections%22%2C%22grams%22%2C%22tags%22%2C%22collection_ids%22%2C%22vendor%22%2C%22named_tags.categories%22%2C%22price%22%2C%22named_tags.breed%20size%22%2C%22named_tags.benefits%22%2C%22named_tags.lifestyle%22%2C%22named_tags.life%20stage%22%2C%22inventory_available%22%5D&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=16&maxValuesPerFacet=50&page={page}&query=&tagFilters="}},{{"indexName":"shopify_pc1_products","params":"analytics=false&clickAnalytics=false&facets=collections&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=0&maxValuesPerFacet=50&page={page}&query="}}]}}"""
)
