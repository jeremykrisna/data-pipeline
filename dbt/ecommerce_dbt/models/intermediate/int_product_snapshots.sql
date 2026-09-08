{{ config(
    materialized='incremental'
) }}

SELECT
    product_id,
    product_name,
    category,
    brand,
    sku,

    price,
    discount_percentage,

    ROUND(
        price * discount_percentage / 100,
        2
    ) AS discount_amount,

    ROUND(
        price * (1 - discount_percentage / 100),
        2
    ) AS final_price,

    rating,
    stock,

    ROUND(
        price * stock,
        2
    ) AS inventory_value,

    snapshot_at

FROM {{ ref('stg_product_snapshots') }}

{% if is_incremental() %}

WHERE snapshot_at > (
    SELECT MAX(snapshot_at)
    FROM {{ this }}
)

{% endif %}