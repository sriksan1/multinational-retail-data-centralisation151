ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(10),
    ALTER COLUMN year TYPE VARCHAR(10),
    ALTER COLUMN day TYPE VARCHAR(10),
    ALTER COLUMN time_period TYPE VARCHAR(10),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;
-- Add primary key constraint to dim_card_details
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);
