import json
from pathlib import Path
from scrapy.exceptions import DropItem
from pydantic import ValidationError

from src.scraper.models import Product

class ProductValidationPipeline:

    def __init__(self):

        self.bad_records = Path(
            "data/quarantine/rejected.json"
        )


    def process_item(self, item, spider):

        try:
            product = Product(**item)

            item.clear()
            item.update(product.model_dump())

            return item


        except ValidationError as e:

            record = {
                "item": dict(item),
                "errors": e.errors()
            }


            with open(
                self.bad_records,
                "a"
            ) as f:

                f.write(
                    json.dumps(record)
                    + "\n"
                )


            spider.logger.warning(
                f"Rejected product {item.get('product_id')}"
            )


            raise DropItem(
                "Invalid product"
            )