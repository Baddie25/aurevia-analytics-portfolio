-- ============================================================
-- Aurevia Group
-- Project 1: Performance Command Center
-- Seed Returns Fact Table
-- ============================================================

INSERT INTO fact_returns (
    order_id,
    sales_id,
    return_date,
    customer_id,
    product_id,
    returned_quantity,
    return_reason,
    refund_amount
)
SELECT
    fs.order_id,
    fs.sales_id,
    LEAST(
        fs.order_date
            + (ABS(HASHTEXT(fs.order_id::TEXT)) % 30),
        DATE '2025-12-31'
    ) AS return_date,
    fs.customer_id,
    fs.product_id,
    1 AS returned_quantity,
    CASE ABS(HASHTEXT(fs.order_id::TEXT)) % 4
        WHEN 0 THEN 'Damaged product'
        WHEN 1 THEN 'Customer preference'
        WHEN 2 THEN 'Incorrect item'
        ELSE 'Product quality'
    END AS return_reason,
    ROUND(
        fs.net_sales_amount / fs.quantity,
        2
    ) AS refund_amount
FROM fact_sales fs
WHERE ABS(HASHTEXT(fs.order_id::TEXT)) % 100 < 8
  AND fs.quantity > 0
  AND NOT EXISTS (
      SELECT 1
      FROM fact_returns fr
      WHERE fr.sales_id = fs.sales_id
  );