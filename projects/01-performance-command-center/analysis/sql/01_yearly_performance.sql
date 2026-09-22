-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Analysis: Yearly Performance
-- ============================================================

SELECT
    EXTRACT(YEAR FROM fs.order_date)::INT AS sales_year,
    COUNT(*) AS sales_lines,
    COUNT(DISTINCT fs.order_id) AS unique_orders,
    COUNT(DISTINCT fs.customer_id) AS active_customers,

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

GROUP BY
    EXTRACT(YEAR FROM fs.order_date)

ORDER BY
    sales_year;


-- ============================================================
-- Year-over-Year Growth
-- ============================================================

WITH yearly AS (
    SELECT
        EXTRACT(YEAR FROM fs.order_date)::INT AS sales_year,
        SUM(fs.net_sales_amount) AS net_revenue,
        SUM(fs.gross_profit_amount) AS gross_profit
    FROM fact_sales fs
    GROUP BY EXTRACT(YEAR FROM fs.order_date)
)

SELECT
    sales_year,

    ROUND(net_revenue, 2) AS net_revenue,
    ROUND(gross_profit, 2) AS gross_profit,

    ROUND(
        (net_revenue - LAG(net_revenue) OVER (ORDER BY sales_year))
        / NULLIF(LAG(net_revenue) OVER (ORDER BY sales_year), 0) * 100,
        2
    ) AS revenue_growth_pct,

    ROUND(
        (gross_profit - LAG(gross_profit) OVER (ORDER BY sales_year))
        / NULLIF(LAG(gross_profit) OVER (ORDER BY sales_year), 0) * 100,
        2
    ) AS gross_profit_growth_pct

FROM yearly

ORDER BY sales_year;