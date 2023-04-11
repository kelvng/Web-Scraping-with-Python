import scrapy
from scrapy.http import FormRequest
import json


class Envato_Spider(scrapy.Spider):
    name = 'envato'
    allowed_domains = ['elements.envato.com']
    start_urls = ["https://elements.envato.com/api/v1/items_page_data.json?type=graphics&page=1&categories=Icons&languageCode=en"]
    custom_settings = {'DOWNLOAD_DELAY': 10}

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,lb;q=0.7",
        "Referer": "https://elements.envato.com/graphics/icons",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "x-csrf-token": "FzQdyGeRcBx7pzHKlf1cTgnf0REoFyGsT619Bxp6nBOECCODv/PRGuONqGRjO/ylPfQFgXKOrE7LUK81R+ydNQ=="
    }
    
    def parse(self, response):
        # yield request
        raw_data = response.body
        data = json.loads(raw_data)
        # for num_page in range(int(data["currentPage"]), int(data["totalPages"]) + 1):
        for num_page in range(int(data["currentPage"]), 51):
            type = 'graphic-templates'
            categories = 'Websites'
            url = 'https://elements.envato.com/api/v1/items_page_data.json?type={0}&page={1}&categories={2}&languageCode=en'.format(type, num_page, categories)
            request = scrapy.Request(url, callback=self.parse_item, headers=self.headers)
            yield request

    def parse_item(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        for item in data["items"]:
            if item['isCurrentlyFree'] == 'true':
                yield {"Name": item["title"],
                       "Link": "https://elements.envato.com/" + item["slug"] + "-" + item["id"]}