import scrapy


class ProductItem(scrapy.Item):
    # Core product details
    id = scrapy.Field()
    gid = scrapy.Field()
    vendor = scrapy.Field()
    type = scrapy.Field()
    handle = scrapy.Field()
    remote = scrapy.Field()
    variants = scrapy.Field()

class CleanedProductItem(scrapy.Item):
    product_id = scrapy.Field()
    handle = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    source_url = scrapy.Field()
    sku = scrapy.Field()
    scraped_at = scrapy.Field()

