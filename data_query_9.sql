WITH TimeDifferences AS (
    SELECT 
        dd.year,
        (CAST(dd.year AS text) || '-' || LPAD(CAST(dd.month AS text), 2, '0') || '-' || LPAD(CAST(dd.day AS text), 2, '0') || ' ' || dd.timestamp)::timestamp AS sale_timestamp,
        LEAD((CAST(dd.year AS text) || '-' || LPAD(CAST(dd.month AS text), 2, '0') || '-' || LPAD(CAST(dd.day AS text), 2, '0') || ' ' || dd.timestamp)::timestamp) OVER (PARTITION BY dd.year ORDER BY dd.year, dd.month, dd.day, dd.timestamp) AS next_sale_timestamp
    FROM 
        orders_table ot
    JOIN 
        dim_date_times dd ON ot.date_uuid = dd.date_uuid
)
, AveragedDifferences AS (
    SELECT 
        year, 
        AVG(EXTRACT(EPOCH FROM (next_sale_timestamp - sale_timestamp))) AS avg_diff_seconds
    FROM 
        TimeDifferences
    WHERE 
        next_sale_timestamp IS NOT NULL
    GROUP BY 
        year
)
SELECT 
    year, 
    CONCAT(
        '"hours": ', FLOOR(avg_diff_seconds / 3600), ', ',
        '"minutes": ', FLOOR((avg_diff_seconds % 3600) / 60), ', ',
        '"seconds": ', FLOOR(avg_diff_seconds % 60), ', ',
        '"milliseconds": ', (avg_diff_seconds - FLOOR(avg_diff_seconds)) * 1000
    ) AS actual_time_taken
FROM 
    AveragedDifferences
ORDER BY 
    avg_diff_seconds DESC
LIMIT 5;
