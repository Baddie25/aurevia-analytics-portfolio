
-- ============================================================
-- AUREVIA GROUP
-- Project 1: Enterprise Performance Command Center
-- Synthetic monthly planning targets
--
-- IMPORTANT:
-- These targets are illustrative planning benchmarks derived
-- from simulated historical sales. They are not approved budgets
-- or evidence of actual historical business targets.
--
-- Target grain: month x division x region x channel.
-- Revenue and gross profit targets: 5% above actuals.
-- Order target: 5% above distinct actual orders, rounded up.
-- ============================================================

BEGIN;

WITH monthly_actuals AS (
    SELECT
        DATE_TRUNC('month', fs.order_date)::date AS target_date,
        p.division_id,
        country.region_id,
        c.channel_id,
        SUM(fs.net_sales_amount) AS baseline_revenue,
        SUM(fs.gross_profit_amount) AS baseline_gross_profit,
        COUNT(DISTINCT fs.order_id) AS baseline_orders
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
INSERT INTO fact_targets (
    target_date,
    division_id,
    region_id,
    channel_id,
    revenue_target,
    gross_profit_target,
    order_target
)
SELECT
    target_date,
    division_id,
    region_id,
    channel_id,
    ROUND(baseline_revenue * 1.05, 2),
    ROUND(baseline_gross_profit * 1.05, 2),
    CEIL(baseline_orders * 1.05)::integer
FROM monthly_actuals
ON CONFLICT (target_date, division_id, region_id, channel_id)
DO NOTHING;

COMMIT;