import scrapy
from urllib.parse import urlparse
from src.scraper.items import CleanedProductItem
from src.scraper.parsers.product_parser import parse_products
from src.scraper.models import Product

class SupermartSpider(scrapy.Spider):

    name = "supermart"
    
    # Crucial: Allow both variations of the domain just in case of automatic middleware redirects
    allowed_domains = ["supermart.ng", "www.supermart.ng"]

    start_urls = [
        "https://www.supermart.ng/collections/uk-groceries?page=1",
        "https://www.supermart.ng/collections/fresh-food?page=1",
        "https://www.supermart.ng/collections/naija-food?page=1",
        "https://www.supermart.ng/collections/mile-12-market?page=1",
        "https://www.supermart.ng/collections/food-cupboard?page=1",
        "https://www.supermart.ng/collections/oil-sauces?page=1",
        "https://www.supermart.ng/collections/drinks?page=1",
        "https://www.supermart.ng/collections/alcohol?page=1",
        "https://www.supermart.ng/collections/toiletries?page=1",
        "https://www.supermart.ng/collections/cleaning?page=1",
        "https://www.supermart.ng/collections/household?page=1",
        "https://www.supermart.ng/collections/frozen?page=1",
        "https://www.supermart.ng/collections/kitchen-dining?page=1",
        "https://www.supermart.ng/collections/health-wellness?page=1",
        "https://www.supermart.ng/collections/baby-kids?page=1",
        "https://www.supermart.ng/collections/office-supplies?page=1",
        "https://www.supermart.ng/collections/electronics?page=1"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"page": 1})

    def parse(self, response):
        current_page = response.meta.get("page", 1)
        self.logger.info(f"--- PARSING: {response.url} (Tracked Page: {current_page}) ---")

        products = parse_products(response.text)

        if not products:
            self.logger.warning(
                f"No products found on {response.url}. Stopping pagination branch."
            )
            return

        for product in products:
            yield product
            # product = Product(**product)
            # yield product.model_dump()

         # 2. Hardcoded Pagination handling
        next_page = current_page + 1
        
        # Reconstruct the string cleanly
        parsed_url = urlparse(response.url)
        base_path = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        next_url = f"{base_path}?page={next_page}"

        self.logger.info(f"Attempting queue for next page: {next_url}")

        yield scrapy.Request(
            url=next_url,
            callback=self.parse,
            meta={"page": next_page},
            dont_filter=True 
        )