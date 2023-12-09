ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN card_number TYPE VARCHAR(max_length_card_number), -- Replace with actual max length
    ALTER COLUMN store_code TYPE VARCHAR(max_length_store_code),   -- Replace with actual max length
    ALTER COLUMN product_code TYPE VARCHAR(max_length_product_code), -- Replace with actual max length
    ALTER COLUMN product_quantity TYPE SMALLINT;
-- Create foreign key constraint for date_uuid
ALTER TABLE orders_table
ADD CONSTRAINT fk_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times(date_uuid);

-- Create foreign key constraint for user_uuid
ALTER TABLE orders_table
ADD CONSTRAINT fk_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users(user_uuid);

-- Create foreign key constraint for card_number
ALTER TABLE orders_table
ADD CONSTRAINT fk_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

-- Create foreign key constraint for product_code
ALTER TABLE orders_table
ADD CONSTRAINT fk_product_code
FOREIGN KEY (product_code)
REFERENCES dim_products(product_code);

-- Update orders_table to include only valid product codes
DELETE FROM orders_table
WHERE product_code NOT IN (SELECT product_code FROM dim_products);

-- Update orders_table to include only valid product codes
DELETE FROM orders_table
WHERE card_number NOT IN (SELECT card_number FROM dim_card_details);
