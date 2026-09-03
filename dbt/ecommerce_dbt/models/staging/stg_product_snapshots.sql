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

    source_file,
    snapshot_at,
    ingested_at

FROM {{ source('bronze', 'bronze_products') }}