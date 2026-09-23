-- ============================================================
-- Analysis 07: Profitability Performance
-- ============================================================
--
-- Business Question:
-- Which divisions, channels, products, and customers generate the most
-- gross profit and strongest gross margins, and where is Aurevia generating
-- revenue without sufficient profitability?
--
-- Purpose:
-- Assess profitability after discounts and product costs, identifying
-- where revenue translates into gross profit and where margins are weaker.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Enterprise Profitability
-- ------------------------------------------------------------

SELECT
    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.product_cost_amount), 2) AS product_cost,

    ROUND(SUM(fs.gross_profit_amount), 2) AS gross_profit,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct

FROM fact_sales fs;


-- ------------------------------------------------------------
-- 2. Profitability by Division
-- ------------------------------------------------------------

SELECT
    d.division_name,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.product_cost_amount), 2) AS product_cost,

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
    d.division_name

ORDER BY
    gross_profit DESC;


-- ------------------------------------------------------------
-- 3. Profitability by Channel
-- ------------------------------------------------------------

SELECT
    ch.channel_name,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.product_cost_amount), 2) AS product_cost,

    ROUND(SUM(fs.gross_profit_amount), 2) AS gross_profit,

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
    gross_profit DESC;


-- ------------------------------------------------------------
-- 4. Profitability by Product
-- ------------------------------------------------------------

SELECT
    p.product_name,
    p.category_name,
    d.division_name,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.product_cost_amount), 2) AS product_cost,

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
    gross_profit DESC;


-- ------------------------------------------------------------
-- 5. Profitability by Customer
-- ------------------------------------------------------------

SELECT
    c.customer_name,
    c.customer_segment,

    COUNT(DISTINCT fs.order_id) AS unique_orders,

    ROUND(SUM(fs.net_sales_amount), 2) AS net_revenue,

    ROUND(SUM(fs.product_cost_amount), 2) AS product_cost,

    ROUND(SUM(fs.gross_profit_amount), 2) AS gross_profit,

    ROUND(
        SUM(fs.gross_profit_amount)
        / NULLIF(SUM(fs.net_sales_amount), 0) * 100,
        2
    ) AS gross_margin_pct

FROM fact_sales fs

JOIN dim_customer c
    ON fs.customer_id = c.customer_id

GROUP BY
    c.customer_name,
    c.customer_segment

ORDER BY
    gross_profit DESC;