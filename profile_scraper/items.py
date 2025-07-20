import scrapy

class ProfileEducationItem(scrapy.Item):
    item_url = scrapy.Field()
    title = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()