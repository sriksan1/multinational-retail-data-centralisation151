SELECT 
    SUM(p.product_price * o.product_quantity) AS total_sales, 
    d.store_type, 
    d.country_code
FROM 
    orders_table o
JOIN 
    dim_products p ON o.product_code = p.product_code
JOIN 
    dim_store_details d ON o.store_code = d.store_code
WHERE 
    d.country_code = 'DE'
GROUP BY 
    d.store_type, d.country_code
ORDER BY 
    total_sales ASC;
