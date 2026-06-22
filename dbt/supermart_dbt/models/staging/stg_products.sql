SELECT
    product_id,
    handle,
    name,
    SAFE_CAST(price AS FLOAT64) AS price,
    category,
    availability,
    source_url,
    sku,
    TIMESTAMP(scraped_at) AS scraped_at,
FROM `infack.supermart_dw.raw_products`
WHERE product_id IS NOT NULL