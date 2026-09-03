SELECT
    product_id,
    snapshot_at,
    COUNT(*) AS row_count
FROM {{ ref('fct_inventory') }}
GROUP BY
    product_id,
    snapshot_at
HAVING COUNT(*) > 1