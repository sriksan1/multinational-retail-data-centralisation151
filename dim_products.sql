-- Remove '£' from product_price and convert to FLOAT
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')::FLOAT;

-- Add new column weight_class
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(255);

-- Populate weight_class based on weight ranges
UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
END;

-- #Part 2
-- Rename a column to still_available
ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
    ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT,
    ALTER COLUMN "EAN" TYPE VARCHAR(17), -- Replace 17 with the actual max length for EAN
    ALTER COLUMN product_code TYPE VARCHAR(11), -- Replace 11 with the actual max length for product_code
    ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
    
    ALTER COLUMN weight_class TYPE VARCHAR(14); -- Replace 14 with the actual max length for weight_class
-- Add primary key constraint to dim_card_details
ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);
