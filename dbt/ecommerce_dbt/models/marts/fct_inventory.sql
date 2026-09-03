SELECT
    product_id,
    snapshot_at,

    price,
    discount_percentage,
    discount_amount,
    final_price,

    stock,
    inventory_value,
    rating

FROM {{ ref('int_product_snapshots') }}