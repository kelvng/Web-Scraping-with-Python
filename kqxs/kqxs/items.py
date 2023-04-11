# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KqxsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class facebook_get_all_self_groups(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class XsktItem(scrapy.Item):
    xs_info = scrapy.Field()
    xs_data = scrapy.Field()

class facebook_scraper(scrapy.Item):
    pass