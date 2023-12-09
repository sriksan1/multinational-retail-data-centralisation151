-- Step 1: Merge Two Latitude Columns
-- Assuming latitude1 and latitude2 are the column names, and we are keeping latitude1
UPDATE store_details_table
SET latitude1 = COALESCE(latitude1, latitude2)
WHERE latitude1 IS NULL;

ALTER TABLE store_details_table
DROP COLUMN latitude2;

-- Rename latitude1 to latitude if it's not already named latitude
ALTER TABLE store_details_table
RENAME COLUMN latitude1 TO latitude;

-- Step 2: Alter Data Types of Various Columns
-- Replace 'max_length_store_code' and 'max_length_country_code' with actual maximum lengths for store_code and country_code
ALTER TABLE store_details_table
    ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT,
    ALTER COLUMN locality TYPE VARCHAR(255),
    ALTER COLUMN store_code TYPE VARCHAR(max_length_store_code),
    ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
    ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
    ALTER COLUMN store_type TYPE VARCHAR(255),
    ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT,
    ALTER COLUMN country_code TYPE VARCHAR(max_length_country_code),
    ALTER COLUMN continent TYPE VARCHAR(255);

-- Step 3: Update Null Values in a Specific Column
-- Assuming the column to update is 'location'
UPDATE store_details_table
SET location = 'N/A'
WHERE location IS NULL;

-- Add primary key constraint to dim_card_details
ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);
