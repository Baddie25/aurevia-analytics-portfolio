-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Seed Sales Fact Table
-- ============================================================

INSERT INTO fact_sales (
    order_id,
    order_line_number,
    order_date,
    customer_id,
    product_id,
    salesperson_id,
    quantity,
    unit_list_price,
    discount_amount,
    unit_cost,
    gross_sales_amount,
    net_sales_amount,
    product_cost_amount,
    gross_profit_amount
)
SELECT
    'ORD-' || LPAD(o.order_num::TEXT, 6, '0') AS order_id,

    l.line_num AS order_line_number,

    o.order_date,

    c.customer_id,

    p.product_id,

    sp.salesperson_id,

    l.quantity,

    pricing.unit_list_price,

    pricing.discount_amount,

    p.standard_cost AS unit_cost,

    pricing.gross_sales_amount,

    pricing.net_sales_amount,

    pricing.product_cost_amount,

    pricing.net_sales_amount - pricing.product_cost_amount
        AS gross_profit_amount

FROM (
    SELECT
        order_num,
        DATE '2022-01-01'
            + ((order_num * 13) % 1461) AS order_date
    FROM generate_series(1, 1500) AS numbers(order_num)
) o

CROSS JOIN LATERAL (
    SELECT
        line_num,
        1 + ((o.order_num + line_num * 3) % 8) AS quantity
    FROM generate_series(
        1,
        1 + (o.order_num % 3)
    ) AS lines(line_num)
) l

JOIN dim_customer c
    ON c.customer_id =
        1 + ((o.order_num * 5 + l.line_num) % 24)

JOIN dim_product p
    ON p.product_id =
        1 + ((o.order_num + l.line_num * 3) % 12)

JOIN dim_salesperson sp
    ON sp.salesperson_id =
        1 + ((o.order_num * 3) % 12)

CROSS JOIN LATERAL (
    SELECT
        ROUND(
            p.list_price *
            CASE
                WHEN (o.order_num % 10) < 3 THEN 0.95
                WHEN (o.order_num % 10) < 5 THEN 0.90
                WHEN (o.order_num % 10) = 9 THEN 0.85
                ELSE 1.00
            END,
            2
        ) AS unit_list_price
) base_price

CROSS JOIN LATERAL (
    SELECT
        ROUND(
            l.quantity * base_price.unit_list_price,
            2
        ) AS gross_sales_amount,

        ROUND(
            l.quantity * base_price.unit_list_price *
            CASE
                WHEN (o.order_num % 10) < 3 THEN 0.05
                WHEN (o.order_num % 10) < 5 THEN 0.10
                WHEN (o.order_num % 10) = 9 THEN 0.15
                ELSE 0.00
            END,
            2
        ) AS discount_amount
) sales_calculation

CROSS JOIN LATERAL (
    SELECT
        base_price.unit_list_price,

        sales_calculation.gross_sales_amount,

        sales_calculation.discount_amount,

        ROUND(
            sales_calculation.gross_sales_amount
            - sales_calculation.discount_amount,
            2
        ) AS net_sales_amount,

        ROUND(
            l.quantity * p.standard_cost,
            2
        ) AS product_cost_amount
) pricing

ON CONFLICT (order_id, order_line_number) DO NOTHING;