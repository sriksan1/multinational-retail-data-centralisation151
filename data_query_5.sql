WITH SalesData AS (
    SELECT 
        CASE 
            WHEN o.store_code LIKE 'WEB%' THEN 'Web portal' 
            ELSE d.store_type 
        END AS store_type,
        SUM(p.product_price * o.product_quantity) AS total_sales
    FROM 
        orders_table o
    JOIN 
        dim_products p ON o.product_code = p.product_code
    LEFT JOIN 
        dim_store_details d ON o.store_code = d.store_code
    GROUP BY 
        CASE 
            WHEN o.store_code LIKE 'WEB%' THEN 'Web portal' 
            ELSE d.store_type 
        END
),
TotalSales AS (
    SELECT SUM(total_sales) AS overall_total FROM SalesData
)
SELECT 
    s.store_type, 
    s.total_sales, 
    (s.total_sales / t.overall_total) * 100 AS percentage_total
FROM 
    SalesData s, TotalSales t
ORDER BY 
    s.total_sales DESC
LIMIT 5;