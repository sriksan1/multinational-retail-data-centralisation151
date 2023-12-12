SELECT 
    COUNT(*) AS numbers_of_sales,
    SUM(product_quantity) AS product_quantity_count,
    CASE 
        WHEN store_code LIKE 'WEB%' THEN 'Web'
        ELSE 'Offline'
    END AS location
FROM 
    orders_table
GROUP BY 
    CASE 
        WHEN store_code LIKE 'WEB%' THEN 'Web'
        ELSE 'Offline'
    END
ORDER BY 
    location;
