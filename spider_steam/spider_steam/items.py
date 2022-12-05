import scrapy


class SpiderSteamItem(scrapy.Item):
    name_of_product = scrapy.Field()
    category_of_product = scrapy.Field()
    rating_of_product = scrapy.Field()
    date_of_release_of_product = scrapy.Field()
    developers_of_product = scrapy.Field()
    tags_of_product = scrapy.Field()
    price_of_product = scrapy.Field()
    platforms_of_product = scrapy.Field()
