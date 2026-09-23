-- ============================================================
-- Project 1: Enterprise Performance Command Center
-- Analysis 06: Discount Performance
-- ============================================================

-- Business Questions:
-- 1. What is Aurevia's overall discount exposure?
-- 2. How does discounting vary across divisions and channels?
-- 3. Where is higher discounting associated with lower
--    revenue realization or gross margins?
--
-- Note:
-- This analysis identifies associations and does not establish
-- that discounting causes changes in revenue or profitability.

-- ============================================================
-- 1. ENTERPRISE-LEVEL DISCOUNT PERFORMANCE
-- ============================================================

SELECT
    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(
        SUM(fs.gross_sales_amount),
        2
    ) AS gross_revenue,

    ROUND(
        SUM(fs.discount_amount),
        2
    ) AS discounts,

    ROUND(
        SUM(fs.net_sales_amount),
        2
    ) AS net_revenue,

    ROUND(
        SUM(fs.gross_profit_amount),
        2
    ) AS gross_profit,

    ROUND(
        SUM(fs.discount_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS discount_rate_pct,

    ROUND(
        SUM(fs.net_sales_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS revenue_realization_pct,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct

FROM fact_sales fs;


-- ============================================================
-- 2. DIVISION × CHANNEL DISCOUNT PERFORMANCE
-- ============================================================

SELECT
    d.division_name,
    ch.channel_name,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(
        SUM(fs.gross_sales_amount),
        2
    ) AS gross_revenue,

    ROUND(
        SUM(fs.discount_amount),
        2
    ) AS discounts,

    ROUND(
        SUM(fs.net_sales_amount),
        2
    ) AS net_revenue,

    ROUND(
        SUM(fs.gross_profit_amount),
        2
    ) AS gross_profit,

    ROUND(
        SUM(fs.discount_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS discount_rate_pct,

    ROUND(
        SUM(fs.net_sales_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS revenue_realization_pct,

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
    discount_rate_pct DESC;

-- ============================================================
-- 3. DIVISION-LEVEL DISCOUNT PERFORMANCE
-- ============================================================

SELECT
    d.division_name,

    ROUND(
        SUM(fs.gross_sales_amount),
        2
    ) AS gross_revenue,

    ROUND(
        SUM(fs.discount_amount),
        2
    ) AS discounts,

    ROUND(
        SUM(fs.discount_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS discount_rate_pct,

    ROUND(
        SUM(fs.net_sales_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS revenue_realization_pct,

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
    d.division_name

ORDER BY
    discount_rate_pct DESC;


-- ============================================================
-- 4. CHANNEL-LEVEL DISCOUNT PERFORMANCE
-- ============================================================

SELECT
    ch.channel_name,

    ROUND(
        SUM(fs.gross_sales_amount),
        2
    ) AS gross_revenue,

    ROUND(
        SUM(fs.discount_amount),
        2
    ) AS discounts,

    ROUND(
        SUM(fs.discount_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS discount_rate_pct,

    ROUND(
        SUM(fs.net_sales_amount)
        / NULLIF(SUM(fs.gross_sales_amount), 0) * 100,
        2
    ) AS revenue_realization_pct,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct

FROM fact_sales fs

JOIN dim_customer c
    ON fs.customer_id = c.customer_id

JOIN dim_channel ch
    ON c.channel_id = ch.channel_id

GROUP BY
    ch.channel_name

ORDER BY
    discount_rate_pct DESC;