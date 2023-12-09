-- Find the maximum length of the card_number column
SELECT MAX(LENGTH(card_number)) AS max_card_number_length FROM dim_card_details;

-- Find the maximum length of the expiry_date column
SELECT MAX(LENGTH(expiry_date)) AS max_expiry_date_length FROM dim_card_details;
-- Replace the ? with the actual maximum lengths you found from the above queries
SELECT date_payment_confirmed
FROM dim_card_details
WHERE date_payment_confirmed IS NOT NULL AND NOT (date_payment_confirmed ~ '^\d{4}-\d{2}-\d{2}$');

SELECT date_payment_confirmed
FROM dim_card_details
WHERE date_payment_confirmed IS NOT NULL AND NOT (date_payment_confirmed ~ '^\d{4}-\d{2}-\d{2}$');

ALTER TABLE dim_card_details
MODIFY card_number VARCHAR(22),  -- Replace with the actual number
MODIFY expiry_date VARCHAR(10),  -- Replace with the actual number
MODIFY date_payment_confirmed DATE;

-- Add primary key constraint to dim_card_details
ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);
