import scrapy


class TestWordItem(scrapy.Item):
    # define the fields for your item here like:

    title = scrapy.Field()
    date = scrapy.Field()
    head = scrapy.Field()
    author = scrapy.Field()
    url_post = scrapy.Field()
    begin = scrapy.Field()
    content = scrapy.Field()
