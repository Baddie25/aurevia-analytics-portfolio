-- ============================================================
-- Project 1: Enterprise Performance Command Center
-- Analysis 05: Customer Performance
-- ============================================================

-- Business Questions:
-- 1. Which customers create the most revenue and gross profit?
-- 2. How does customer profitability vary across the customer base?
-- 3. How concentrated is Aurevia's customer revenue?
-- 4. How do customer segments differ in scale and economics?

-- ============================================================
-- 1. CUSTOMER-LEVEL PERFORMANCE
-- ============================================================

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
    ) AS average_order_value,

    ROUND(
        SUM(fs.net_sales_amount)
        / NULLIF(
            SUM(SUM(fs.net_sales_amount)) OVER (),
            0
        ) * 100,
        2
    ) AS revenue_share_pct

FROM fact_sales fs

JOIN dim_customer c
    ON fs.customer_id = c.customer_id

GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_segment

ORDER BY
    net_revenue DESC;


-- ============================================================
-- 2. CUSTOMER-SEGMENT PERFORMANCE
-- ============================================================

SELECT
    c.customer_segment,

    COUNT(DISTINCT c.customer_id) AS customers,

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
        / NULLIF(COUNT(DISTINCT c.customer_id), 0),
        2
    ) AS revenue_per_customer

FROM fact_sales fs

JOIN dim_customer c
    ON fs.customer_id = c.customer_id

GROUP BY
    c.customer_segment

ORDER BY
    net_revenue DESC;