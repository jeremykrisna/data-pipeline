WITH products AS (

    SELECT *
    FROM {{ ref('stg_products') }}

)

SELECT
    product_id,
    product_name,
    description,
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

    weight,

    warranty_information,
    shipping_information,
    availability_status,
    return_policy,
    minimum_order_quantity,

    snapshot_at

FROM products