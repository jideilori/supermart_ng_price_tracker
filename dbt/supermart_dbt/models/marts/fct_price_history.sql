SELECT
    product_id,
    name,
    price,
    scraped_at,
    LAG(price) OVER (
        PARTITION BY product_id
        ORDER BY scraped_at
    ) AS previous_price,
    price - LAG(price) OVER (
        PARTITION BY product_id
        ORDER BY scraped_at
    ) AS price_change
FROM {{ ref('stg_products') }}