SELECT 
    SUM(o.product_quantity * p.product_price) AS total_sales, 
    d.month 
FROM 
    orders_table o
JOIN 
    dim_products p ON o.product_code = p.product_code
JOIN 
    dim_date_times d ON o.date_uuid = d.date_uuid
GROUP BY 
    d.month
ORDER BY 
    total_sales DESC
LIMIT 6;