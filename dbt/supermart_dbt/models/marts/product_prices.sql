SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY product_id
               ORDER BY scraped_at DESC
           ) AS rn
    FROM {{ ref('stg_products') }}
)
WHERE rn = 1