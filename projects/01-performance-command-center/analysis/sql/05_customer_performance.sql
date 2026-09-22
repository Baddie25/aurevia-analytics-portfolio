-- ============================================================
-- Project 1: Enterprise Performance Command Center
-- Analysis 05: Customer Performance
-- ============================================================

-- Business Question:
-- Which customers create the most revenue and gross profit for
-- Aurevia, and how does customer profitability vary across
-- the customer base?

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_segment,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(
        SUM(fs.net_sales_amount),
        2
    ) AS net_revenue,

    ROUND(
        SUM(fs.gross_profit_amount),
        2
    ) AS gross_profit,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct,

    ROUND(
        SUM(fs.net_sales_amount)
        / NULLIF(COUNT(DISTINCT fs.order_id), 0),
        2
    ) AS average_order_value

FROM fact_sales fs

JOIN dim_customer c
    ON fs.customer_id = c.customer_id

GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_segment

ORDER BY
    net_revenue DESC;