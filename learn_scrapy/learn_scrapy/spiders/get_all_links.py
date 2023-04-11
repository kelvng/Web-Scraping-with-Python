import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

class get_all_links_spider(CrawlSpider):
    name = "get_all_links"
    custom_settings = {
        'DEPTH_LIMIT': 0
    }
    allowed_domains = ["vietnamnet.vn"]
    start_urls = ["https://vietnamnet.vn"]
    base_url = "https://vietnamnet.vn"
    rules = [
        Rule(
            LinkExtractor(
                allow_domains="vietnamnet.vn",
                unique=True
            ),
            follow = True,
            callback="parse"
        )
    ]

    def parse(self, response):
        for link in LinkExtractor().extract_links(response):
            yield {"link": link.url}