import pytest
from scrapy.exceptions import DropItem

from src.scraper.models import Product
from src.scraper.pipelines.product_validation import ProductValidationPipeline


@pytest.fixture
def valid_item():
    return {
        "product_id": "101",
        "handle": "banana",
        "name": "Banana",
        "price": 2.5,
        "category": "Fruit",
        "source_url": "https://www.supermart.ng/products/banana",
        "sku": "SKU-1",
        "scraped_at": "2026-06-24T10:00:00",
    }


def test_product_model_accepts_valid_payload(valid_item):
    product = Product(**valid_item)

    assert product.product_id == "101"
    assert product.price == 2.5
    assert product.availability is True


def test_product_model_rejects_non_positive_price(valid_item):
    invalid_item = dict(valid_item)
    invalid_item["price"] = 0

    with pytest.raises(Exception):
        Product(**invalid_item)


def test_validation_pipeline_accepts_valid_item(valid_item):
    pipeline = ProductValidationPipeline()
    class DummySpider:
        logger = type("Logger", (), {"warning": staticmethod(lambda *args, **kwargs: None)})()

    item = dict(valid_item)
    processed = pipeline.process_item(item, DummySpider())

    assert processed["product_id"] == "101"
    assert processed["price"] == 2.5


def test_validation_pipeline_drops_invalid_item(valid_item):
    pipeline = ProductValidationPipeline()

    class DummySpider:
        logger = type("Logger", (), {"warning": staticmethod(lambda *args, **kwargs: None)})()

    invalid_item = dict(valid_item)
    invalid_item["price"] = 0

    with pytest.raises(DropItem):
        pipeline.process_item(invalid_item, DummySpider())
