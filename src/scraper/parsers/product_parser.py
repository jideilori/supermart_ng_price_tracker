import re
import json
import logging
from datetime import datetime
from src.scraper.items import CleanedProductItem, ProductItem



logger = logging.getLogger(__name__)


def parse_products(html: str):
    """
    Extract Shopify embedded product JSON safely.
    """

    # More robust regex (avoids greedy JSON breakage)
    pattern = r"var\s+meta\s*=\s*(\{[\s\S]*?\});"

    match = re.search(pattern, html)

    if not match:
        logger.warning("No Shopify meta object found in HTML")
        return []

    raw_json = match.group(1)

    try:
        data = json.loads(raw_json)

    except json.JSONDecodeError:
        logger.error("Failed to parse Shopify meta JSON")
        return []

    products = data.get("products", [])

    # Normalize output immediately (important upgrade)
    # return normalize_products(products)
    return [CleanedProductItem(**product) for product in normalize_products(products)]

def normalize_products(products: ProductItem):
    cleaned = []
    for p in products:
    
        cleaned.append({
            "product_id": str(p.get("id")),
            "handle": p.get('handle'),
            "name": p.get("variants")[0]['name'],
            "price": extract_price(p.get('variants')[0]),
            "category": p.get('type'),
            "source_url": build_url(p),
            "sku": p.get('variants')[0].get('sku'),
            "scraped_at": datetime.now().isoformat()
        })
        
    return cleaned



def extract_price(product: dict):
    price = product.get("price")

    if price is None:
        return None

    try:
        return float(price) / 100  
    except:
        return None


def build_url(product: dict):
    handle = product.get("handle")
    if not handle:
        return None

    return f"https://www.supermart.ng/products/{handle}"