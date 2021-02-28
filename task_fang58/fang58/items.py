import scrapy


class Fang58Item(scrapy.Item):
    """
    房源基本信息
    """
    url = scrapy.Field()
    info = scrapy.Field()
    price = scrapy.Field()
    per_price = scrapy.Field()
    location = scrapy.Field()
    people = scrapy.Field()
