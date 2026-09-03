WITH source AS (

    SELECT *
    FROM {{ source('bronze', 'bronze_products') }}

),

latest AS (

    SELECT
        *
    FROM source

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY id
        ORDER BY snapshot_at DESC
    ) = 1

)

SELECT
    id AS product_id,
    title AS product_name,
    description,
    category,
    brand,
    sku,

    price,
    discountPercentage AS discount_percentage,
    rating,
    stock,

    weight,

    dimensions,
    tags,
    images,

    warrantyInformation AS warranty_information,
    shippingInformation AS shipping_information,
    availabilityStatus AS availability_status,
    returnPolicy AS return_policy,
    minimumOrderQuantity AS minimum_order_quantity,

    reviews,
    meta,
    thumbnail,

    snapshot_at

FROM latest