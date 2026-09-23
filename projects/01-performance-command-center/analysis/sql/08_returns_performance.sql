-- ============================================================
-- Analysis 08: Returns Performance
-- ============================================================
--
-- Business Question:
-- How much revenue and profit is Aurevia losing through product
-- returns, and where are return rates concentrated across
-- products, divisions, channels, customers, and geographies?
--
-- Analytical principle:
-- Aggregate sales and returns independently before joining
-- to prevent row multiplication and duplicated amounts.
--
-- Return Rate:
-- Returned Units / Units Sold
--
-- Estimated Gross Profit Impact:
-- Refund Amount - Estimated Product Cost of Returned Units
--
-- ============================================================


-- ============================================================
-- 1. OVERALL RETURN PERFORMANCE
-- Validation note:
-- Sales and returns are aggregated separately before calculating
-- return rates. Joining fact_returns directly to fact_sales would
-- restrict the denominator to returned transactions and overstate
-- the overall return rate.
-- ============================================================



WITH sales_summary AS (
    SELECT
        SUM(quantity) AS units_sold,
        SUM(net_sales_amount) AS net_revenue,
        SUM(gross_profit_amount) AS gross_profit
    FROM fact_sales
),

returns_summary AS (
    SELECT
        SUM(returned_quantity) AS units_returned,
        SUM(refund_amount) AS refund_amount
    FROM fact_returns
),

returned_cost AS (
    SELECT
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
)

SELECT
    ss.units_sold,
    rs.units_returned,

    ROUND(
        rs.units_returned::numeric
        / NULLIF(ss.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(ss.net_revenue, 2) AS net_revenue,

    ROUND(rs.refund_amount, 2) AS refund_amount,

    ROUND(rc.returned_product_cost, 2)
        AS estimated_returned_product_cost,

    ROUND(
        rs.refund_amount - rc.returned_product_cost,
        2
    ) AS estimated_gross_profit_impact,

    ROUND(
        (
            rs.refund_amount - rc.returned_product_cost
        )
        / NULLIF(ss.net_revenue, 0) * 100,
        2
    ) AS estimated_gross_profit_impact_pct

FROM sales_summary ss
CROSS JOIN returns_summary rs
CROSS JOIN returned_cost rc;


-- ============================================================
-- 2. RETURN PERFORMANCE BY PRODUCT
-- ============================================================

WITH sales_by_product AS (
    SELECT
        product_id,
        SUM(quantity) AS units_sold,
        SUM(net_sales_amount) AS net_revenue
    FROM fact_sales
    GROUP BY product_id
),

returns_by_product AS (
    SELECT
        product_id,
        SUM(returned_quantity) AS units_returned,
        SUM(refund_amount) AS refund_amount
    FROM fact_returns
    GROUP BY product_id
),

returned_cost_by_product AS (
    SELECT
        fr.product_id,
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
    GROUP BY fr.product_id
)

SELECT
    p.product_name,
    p.category_name,
    d.division_name,

    COALESCE(sp.units_sold, 0) AS units_sold,

    COALESCE(rp.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(rp.units_returned, 0)::numeric
        / NULLIF(sp.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(COALESCE(sp.net_revenue, 0), 2)
        AS net_revenue,

    ROUND(COALESCE(rp.refund_amount, 0), 2)
        AS refund_amount,

    ROUND(
        COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_returned_product_cost,

    ROUND(
        COALESCE(rp.refund_amount, 0)
        - COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_gross_profit_impact

FROM dim_product p

JOIN dim_division d
    ON p.division_id = d.division_id

LEFT JOIN sales_by_product sp
    ON p.product_id = sp.product_id

LEFT JOIN returns_by_product rp
    ON p.product_id = rp.product_id

LEFT JOIN returned_cost_by_product rc
    ON p.product_id = rc.product_id

WHERE COALESCE(rp.units_returned, 0) > 0

ORDER BY return_rate_pct DESC;


-- ============================================================
-- 3. RETURN PERFORMANCE BY DIVISION
-- ============================================================

WITH sales_by_division AS (
    SELECT
        p.division_id,
        SUM(fs.quantity) AS units_sold,
        SUM(fs.net_sales_amount) AS net_revenue
    FROM fact_sales fs
    JOIN dim_product p
        ON fs.product_id = p.product_id
    GROUP BY p.division_id
),

returns_by_division AS (
    SELECT
        p.division_id,
        SUM(fr.returned_quantity) AS units_returned,
        SUM(fr.refund_amount) AS refund_amount
    FROM fact_returns fr
    JOIN dim_product p
        ON fr.product_id = p.product_id
    GROUP BY p.division_id
),

returned_cost_by_division AS (
    SELECT
        p.division_id,
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
    JOIN dim_product p
        ON fr.product_id = p.product_id
    GROUP BY p.division_id
)

SELECT
    d.division_name,

    COALESCE(sd.units_sold, 0) AS units_sold,

    COALESCE(rd.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(rd.units_returned, 0)::numeric
        / NULLIF(sd.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(COALESCE(sd.net_revenue, 0), 2)
        AS net_revenue,

    ROUND(COALESCE(rd.refund_amount, 0), 2)
        AS refund_amount,

    ROUND(
        COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_returned_product_cost,

    ROUND(
        COALESCE(rd.refund_amount, 0)
        - COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_gross_profit_impact

FROM dim_division d

LEFT JOIN sales_by_division sd
    ON d.division_id = sd.division_id

LEFT JOIN returns_by_division rd
    ON d.division_id = rd.division_id

LEFT JOIN returned_cost_by_division rc
    ON d.division_id = rc.division_id

ORDER BY return_rate_pct DESC;


-- ============================================================
-- 4. RETURN PERFORMANCE BY CHANNEL
-- ============================================================

WITH sales_by_channel AS (
    SELECT
        c.channel_id,
        SUM(fs.quantity) AS units_sold,
        SUM(fs.net_sales_amount) AS net_revenue
    FROM fact_sales fs
    JOIN dim_customer c
        ON fs.customer_id = c.customer_id
    GROUP BY c.channel_id
),

returns_by_channel AS (
    SELECT
        c.channel_id,
        SUM(fr.returned_quantity) AS units_returned,
        SUM(fr.refund_amount) AS refund_amount
    FROM fact_returns fr
    JOIN dim_customer c
        ON fr.customer_id = c.customer_id
    GROUP BY c.channel_id
),

returned_cost_by_channel AS (
    SELECT
        c.channel_id,
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
    JOIN dim_customer c
        ON fr.customer_id = c.customer_id
    GROUP BY c.channel_id
)

SELECT
    ch.channel_name,

    COALESCE(sc.units_sold, 0) AS units_sold,

    COALESCE(rc.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(rc.units_returned, 0)::numeric
        / NULLIF(sc.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(COALESCE(sc.net_revenue, 0), 2)
        AS net_revenue,

    ROUND(COALESCE(rc.refund_amount, 0), 2)
        AS refund_amount,

    ROUND(
        COALESCE(rcc.returned_product_cost, 0),
        2
    ) AS estimated_returned_product_cost,

    ROUND(
        COALESCE(rc.refund_amount, 0)
        - COALESCE(rcc.returned_product_cost, 0),
        2
    ) AS estimated_gross_profit_impact

FROM dim_channel ch

LEFT JOIN sales_by_channel sc
    ON ch.channel_id = sc.channel_id

LEFT JOIN returns_by_channel rc
    ON ch.channel_id = rc.channel_id

LEFT JOIN returned_cost_by_channel rcc
    ON ch.channel_id = rcc.channel_id

ORDER BY return_rate_pct DESC;


-- ============================================================
-- 5. RETURN PERFORMANCE BY CUSTOMER
-- ============================================================

WITH sales_by_customer AS (
    SELECT
        customer_id,
        SUM(quantity) AS units_sold,
        SUM(net_sales_amount) AS net_revenue
    FROM fact_sales
    GROUP BY customer_id
),

returns_by_customer AS (
    SELECT
        customer_id,
        SUM(returned_quantity) AS units_returned,
        SUM(refund_amount) AS refund_amount
    FROM fact_returns
    GROUP BY customer_id
),

returned_cost_by_customer AS (
    SELECT
        fr.customer_id,
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
    GROUP BY fr.customer_id
)

SELECT
    c.customer_name,
    c.customer_segment,

    COALESCE(sc.units_sold, 0) AS units_sold,

    COALESCE(rc.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(rc.units_returned, 0)::numeric
        / NULLIF(sc.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(COALESCE(sc.net_revenue, 0), 2)
        AS net_revenue,

    ROUND(COALESCE(rc.refund_amount, 0), 2)
        AS refund_amount,

    ROUND(
        COALESCE(rcc.returned_product_cost, 0),
        2
    ) AS estimated_returned_product_cost,

    ROUND(
        COALESCE(rc.refund_amount, 0)
        - COALESCE(rcc.returned_product_cost, 0),
        2
    ) AS estimated_gross_profit_impact

FROM dim_customer c

LEFT JOIN sales_by_customer sc
    ON c.customer_id = sc.customer_id

LEFT JOIN returns_by_customer rc
    ON c.customer_id = rc.customer_id

LEFT JOIN returned_cost_by_customer rcc
    ON c.customer_id = rcc.customer_id

WHERE COALESCE(rc.units_returned, 0) > 0

ORDER BY return_rate_pct DESC;


-- ============================================================
-- 6. RETURN PERFORMANCE BY REGION
-- ============================================================

WITH sales_by_region AS (
    SELECT
        r.region_id,
        SUM(fs.quantity) AS units_sold,
        SUM(fs.net_sales_amount) AS net_revenue
    FROM fact_sales fs
    JOIN dim_customer cu
        ON fs.customer_id = cu.customer_id
    JOIN dim_country c
        ON cu.country_id = c.country_id
    JOIN dim_region r
        ON c.region_id = r.region_id
    GROUP BY r.region_id
),

returns_by_region AS (
    SELECT
        r.region_id,
        SUM(fr.returned_quantity) AS units_returned,
        SUM(fr.refund_amount) AS refund_amount
    FROM fact_returns fr
    JOIN dim_customer cu
        ON fr.customer_id = cu.customer_id
    JOIN dim_country c
        ON cu.country_id = c.country_id
    JOIN dim_region r
        ON c.region_id = r.region_id
    GROUP BY r.region_id
),

returned_cost_by_region AS (
    SELECT
        r.region_id,
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
    JOIN dim_customer cu
        ON fr.customer_id = cu.customer_id
    JOIN dim_country c
        ON cu.country_id = c.country_id
    JOIN dim_region r
        ON c.region_id = r.region_id
    GROUP BY r.region_id
)

SELECT
    r.region_name,

    COALESCE(sr.units_sold, 0) AS units_sold,

    COALESCE(rr.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(rr.units_returned, 0)::numeric
        / NULLIF(sr.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(COALESCE(sr.net_revenue, 0), 2)
        AS net_revenue,

    ROUND(COALESCE(rr.refund_amount, 0), 2)
        AS refund_amount,

    ROUND(
        COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_returned_product_cost,

    ROUND(
        COALESCE(rr.refund_amount, 0)
        - COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_gross_profit_impact

FROM dim_region r

LEFT JOIN sales_by_region sr
    ON r.region_id = sr.region_id

LEFT JOIN returns_by_region rr
    ON r.region_id = rr.region_id

LEFT JOIN returned_cost_by_region rc
    ON r.region_id = rc.region_id

ORDER BY return_rate_pct DESC;


-- ============================================================
-- 7. RETURN PERFORMANCE BY COUNTRY
-- ============================================================

WITH sales_by_country AS (
    SELECT
        cu.country_id,
        SUM(fs.quantity) AS units_sold,
        SUM(fs.net_sales_amount) AS net_revenue
    FROM fact_sales fs
    JOIN dim_customer cu
        ON fs.customer_id = cu.customer_id
    GROUP BY cu.country_id
),

returns_by_country AS (
    SELECT
        fr.customer_id,
        cu.country_id,
        SUM(fr.returned_quantity) AS units_returned,
        SUM(fr.refund_amount) AS refund_amount
    FROM fact_returns fr
    JOIN dim_customer cu
        ON fr.customer_id = cu.customer_id
    GROUP BY fr.customer_id, cu.country_id
),

country_returns AS (
    SELECT
        country_id,
        SUM(units_returned) AS units_returned,
        SUM(refund_amount) AS refund_amount
    FROM returns_by_country
    GROUP BY country_id
),

returned_cost_by_country AS (
    SELECT
        cu.country_id,
        SUM(
            fr.returned_quantity * fs.unit_cost
        ) AS returned_product_cost
    FROM fact_returns fr
    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id
    JOIN dim_customer cu
        ON fr.customer_id = cu.customer_id
    GROUP BY cu.country_id
)

SELECT
    c.country_name,

    r.region_name,

    COALESCE(sc.units_sold, 0) AS units_sold,

    COALESCE(cr.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(cr.units_returned, 0)::numeric
        / NULLIF(sc.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(COALESCE(sc.net_revenue, 0), 2)
        AS net_revenue,

    ROUND(COALESCE(cr.refund_amount, 0), 2)
        AS refund_amount,

    ROUND(
        COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_returned_product_cost,

    ROUND(
        COALESCE(cr.refund_amount, 0)
        - COALESCE(rc.returned_product_cost, 0),
        2
    ) AS estimated_gross_profit_impact

FROM dim_country c

JOIN dim_region r
    ON c.region_id = r.region_id

LEFT JOIN sales_by_country sc
    ON c.country_id = sc.country_id

LEFT JOIN country_returns cr
    ON c.country_id = cr.country_id

LEFT JOIN returned_cost_by_country rc
    ON c.country_id = rc.country_id

ORDER BY return_rate_pct DESC;


-- ============================================================
-- 8. RETURN PERFORMANCE BY RETURN REASON
-- ============================================================

SELECT
    fr.return_reason,

    COUNT(*) AS return_transactions,

    SUM(fr.returned_quantity) AS units_returned,

    ROUND(
        SUM(fr.refund_amount),
        2
    ) AS refund_amount,

    ROUND(
        SUM(fr.refund_amount)
        / NULLIF(
            SUM(SUM(fr.refund_amount))
            OVER (),
            0
        ) * 100,
        2
    ) AS refund_share_pct

FROM fact_returns fr

GROUP BY fr.return_reason

ORDER BY refund_amount DESC;


-- ============================================================
-- 9. MONTHLY RETURN TREND
-- ============================================================
--
-- Return rate is measured against the month in which the
-- original sale occurred, using sales_id to associate each
-- return with its originating sale.
--
-- This avoids comparing returns recorded in one month with
-- sales recorded in a different month.
-- ============================================================

WITH sales_by_month AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS month,

        SUM(quantity) AS units_sold,

        SUM(net_sales_amount) AS net_revenue

    FROM fact_sales

    GROUP BY
        DATE_TRUNC('month', order_date)
),

returns_by_sale_month AS (
    SELECT
        DATE_TRUNC('month', fs.order_date)::date AS month,

        SUM(fr.returned_quantity) AS units_returned,

        SUM(fr.refund_amount) AS refund_amount

    FROM fact_returns fr

    JOIN fact_sales fs
        ON fr.sales_id = fs.sales_id

    GROUP BY
        DATE_TRUNC('month', fs.order_date)
)

SELECT
    COALESCE(sm.month, rm.month) AS month,

    COALESCE(sm.units_sold, 0) AS units_sold,

    COALESCE(rm.units_returned, 0) AS units_returned,

    ROUND(
        COALESCE(rm.units_returned, 0)::numeric
        / NULLIF(sm.units_sold, 0) * 100,
        2
    ) AS return_rate_pct,

    ROUND(
        COALESCE(sm.net_revenue, 0),
        2
    ) AS net_revenue,

    ROUND(
        COALESCE(rm.refund_amount, 0),
        2
    ) AS refund_amount

FROM sales_by_month sm

FULL OUTER JOIN returns_by_sale_month rm
    ON sm.month = rm.month

ORDER BY
    month;