-- ============================================================
-- Project 01 — Enterprise Performance Command Center
-- Analysis 04 — Product Performance
-- ============================================================
-- Business question:
-- Which products are driving revenue and gross profit,
-- and which products have weaker economic performance?
-- ============================================================

SELECT
    p.product_name,
    p.category_name,
    d.division_name,

    COUNT(*) AS sales_lines,

    SUM(fs.quantity) AS units_sold,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.gross_sales_amount), 2) AS gross_revenue,

    ROUND(SUM(fs.discount_amount), 2) AS discounts,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.gross_profit_amount), 2) AS gross_profit,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct

FROM fact_sales fs

JOIN dim_product p
    ON fs.product_id = p.product_id

JOIN dim_division d
    ON p.division_id = d.division_id

GROUP BY
    p.product_name,
    p.category_name,
    d.division_name

ORDER BY
    net_revenue DESC;