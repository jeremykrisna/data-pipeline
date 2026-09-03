SELECT
    product_id,
    product_name,
    description,
    category,
    brand,
    sku,

    weight,

    warranty_information,
    shipping_information,
    availability_status,
    return_policy,
    minimum_order_quantity

FROM {{ ref('int_products') }}