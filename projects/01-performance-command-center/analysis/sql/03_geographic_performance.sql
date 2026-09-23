-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Analysis 03: Geographic Performance
-- ============================================================

-- Geographic performance is analyzed at three levels:
-- Region → Cluster → Country
--
-- This allows management to distinguish:
-- 1. broad regional performance,
-- 2. cluster-level patterns within regions,
-- 3. country-level variation within clusters.

SELECT
    r.region_name,
    cl.cluster_name,
    c.country_name,

    COUNT(*) AS sales_lines,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.gross_profit_amount), 2) AS gross_profit,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct

FROM fact_sales fs

JOIN dim_customer cu
    ON fs.customer_id = cu.customer_id

JOIN dim_country c
    ON cu.country_id = c.country_id

JOIN dim_cluster cl
    ON c.cluster_id = cl.cluster_id

JOIN dim_region r
    ON c.region_id = r.region_id

GROUP BY
    r.region_name,
    cl.cluster_name,
    c.country_name

ORDER BY
    net_revenue DESC;