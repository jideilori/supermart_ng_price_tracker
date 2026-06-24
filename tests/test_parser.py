import pytest

from src.scraper.items import CleanedProductItem
from src.scraper.parsers.product_parser import build_url, extract_price, parse_products


@pytest.fixture
def sample_html():
    return """
    <html>
      <body>
        <script>
          var meta = {"products":[{"id":101,"handle":"banana","type":"Fruit","variants":[{"name":"Banana","price":"250","sku":"SKU-1"}]}]};
        </script>
      </body>
    </html>
    """


def test_parse_products_returns_empty_list_for_missing_meta_object():
    assert parse_products("<html><body>no meta here</body></html>") == []


def test_parse_products_builds_cleaned_product_from_shopify_meta(sample_html):
    parsed = parse_products(sample_html)

    assert len(parsed) == 1
    assert isinstance(parsed[0], CleanedProductItem)
    assert parsed[0]["product_id"] == "101"
    assert parsed[0]["handle"] == "banana"
    assert parsed[0]["name"] == "Banana"
    assert parsed[0]["price"] == 2.5
    assert parsed[0]["category"] == "Fruit"
    assert parsed[0]["sku"] == "SKU-1"
    assert parsed[0]["source_url"] == "https://www.supermart.ng/products/banana"


def test_extract_price_returns_none_for_missing_or_invalid_price():
    assert extract_price({}) is None
    assert extract_price({"price": "abc"}) is None


def test_build_url_returns_none_when_handle_missing():
    assert build_url({}) is None
