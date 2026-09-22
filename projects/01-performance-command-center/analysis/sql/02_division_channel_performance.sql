-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Analysis 02: Division & Channel Performance
-- ============================================================

SELECT
    d.division_name,
    ch.channel_name,

    COUNT(*) AS sales_lines,

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

JOIN dim_customer c
    ON fs.customer_id = c.customer_id

JOIN dim_channel ch
    ON c.channel_id = ch.channel_id

GROUP BY
    d.division_name,
    ch.channel_name

ORDER BY
    net_revenue DESC;