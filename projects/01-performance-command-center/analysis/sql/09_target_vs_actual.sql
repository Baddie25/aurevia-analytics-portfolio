
-- ============================================================
-- AUREVIA GROUP
-- Project 1: Enterprise Performance Command Center
-- Monthly target versus actual performance
--
-- Targets are synthetic retrospective benchmarks, not approved
-- budgets or genuine historical business targets.
--
-- Grain: month x division x region x channel.
-- Actuals are aggregated before joining to targets.
-- ============================================================

WITH monthly_actuals AS (
    SELECT
        DATE_TRUNC('month', fs.order_date)::date AS target_date,
        p.division_id,
        country.region_id,
        c.channel_id,
        SUM(fs.net_sales_amount) AS actual_revenue,
        SUM(fs.gross_profit_amount) AS actual_gross_profit,
        COUNT(DISTINCT fs.order_id) AS actual_orders
    FROM fact_sales fs
    JOIN dim_product p
        ON fs.product_id = p.product_id
    JOIN dim_customer c
        ON fs.customer_id = c.customer_id
    JOIN dim_country country
        ON c.country_id = country.country_id
    GROUP BY
        DATE_TRUNC('month', fs.order_date)::date,
        p.division_id,
        country.region_id,
        c.channel_id
)
SELECT
    t.target_date,
    d.division_name,
    r.region_name,
    ch.channel_name,

    COALESCE(a.actual_revenue, 0) AS actual_revenue,
    t.revenue_target,
    ROUND(
        COALESCE(a.actual_revenue, 0) - t.revenue_target,
        2
    ) AS revenue_variance,
    ROUND(
        100.0 * (
            COALESCE(a.actual_revenue, 0) - t.revenue_target
        ) / NULLIF(t.revenue_target, 0),
        2
    ) AS revenue_variance_pct,

    COALESCE(a.actual_gross_profit, 0) AS actual_gross_profit,
    t.gross_profit_target,
    ROUND(
        COALESCE(a.actual_gross_profit, 0) - t.gross_profit_target,
        2
    ) AS gross_profit_variance,
    ROUND(
        100.0 * (
            COALESCE(a.actual_gross_profit, 0) - t.gross_profit_target
        ) / NULLIF(t.gross_profit_target, 0),
        2
    ) AS gross_profit_variance_pct,

    COALESCE(a.actual_orders, 0) AS actual_orders,
    t.order_target,
    COALESCE(a.actual_orders, 0) - t.order_target AS order_variance,
    ROUND(
        100.0 * (
            COALESCE(a.actual_orders, 0) - t.order_target
        ) / NULLIF(t.order_target, 0),
        2
    ) AS order_variance_pct

FROM fact_targets t
JOIN dim_division d
    ON t.division_id = d.division_id
JOIN dim_region r
    ON t.region_id = r.region_id
JOIN dim_channel ch
    ON t.channel_id = ch.channel_id
LEFT JOIN monthly_actuals a
    ON t.target_date = a.target_date
    AND t.division_id = a.division_id
    AND t.region_id = a.region_id
    AND t.channel_id = a.channel_id
ORDER BY
    t.target_date,
    d.division_name,
    r.region_name,
    ch.channel_name;