{{ config(materialized='table') }}

SELECT *
FROM warehouse.main.bronze_products