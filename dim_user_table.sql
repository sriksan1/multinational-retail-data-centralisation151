DELETE FROM dim_users 
WHERE NOT (user_uuid ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$') OR user_uuid IS NULL;

ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN country_code TYPE VARCHAR(3), -- Adjusted to 3 based on data requirements
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
    ALTER COLUMN join_date TYPE DATE USING join_date::DATE;

-- Add primary key constraint to dim_card_details
ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);
