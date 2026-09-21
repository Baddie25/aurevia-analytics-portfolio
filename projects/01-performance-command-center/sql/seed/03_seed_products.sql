-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Seed Product Dimension
-- ============================================================

INSERT INTO dim_product (
    product_code,
    product_name,
    category_name,
    division_id,
    standard_cost,
    list_price,
    launch_date,
    is_active
)
SELECT
    p.product_code,
    p.product_name,
    p.category_name,
    d.division_id,
    p.standard_cost,
    p.list_price,
    p.launch_date,
    p.is_active
FROM (
    VALUES
        ('PC-001', 'Hydrating Body Wash', 'Body Care',
         'Personal Care', 3.20, 8.99, DATE '2022-01-15', TRUE),

        ('PC-002', 'Daily Facial Cleanser', 'Skincare',
         'Personal Care', 4.10, 11.99, DATE '2022-03-01', TRUE),

        ('PC-003', 'Nourishing Hand Cream', 'Hand Care',
         'Personal Care', 2.40, 6.99, DATE '2022-05-10', TRUE),

        ('HL-001', 'Scented Home Candle', 'Home Fragrance',
         'Home & Lifestyle', 5.50, 16.99, DATE '2022-02-20', TRUE),

        ('HL-002', 'Multi-Surface Cleaner', 'Home Cleaning',
         'Home & Lifestyle', 2.80, 7.49, DATE '2022-04-15', TRUE),

        ('HL-003', 'Reusable Storage Set', 'Home Organization',
         'Home & Lifestyle', 6.20, 18.99, DATE '2023-01-10', TRUE),

        ('WE-001', 'Daily Vitamin Complex', 'Supplements',
         'Wellness', 7.50, 21.99, DATE '2023-02-01', TRUE),

        ('WE-002', 'Herbal Sleep Support', 'Sleep Wellness',
         'Wellness', 8.20, 24.99, DATE '2023-06-15', TRUE),

        ('WE-003', 'Electrolyte Hydration Mix', 'Sports Wellness',
         'Wellness', 4.80, 14.99, DATE '2024-01-20', TRUE),

        ('EE-001', 'Everyday Laundry Pods', 'Laundry Care',
         'Everyday Essentials', 4.60, 12.99, DATE '2022-01-25', TRUE),

        ('EE-002', 'Kitchen Paper Towels', 'Paper Products',
         'Everyday Essentials', 3.10, 8.49, DATE '2022-06-01', TRUE),

        ('EE-003', 'Household Essentials Bundle', 'Household Bundles',
         'Everyday Essentials', 9.50, 26.99, DATE '2024-03-15', TRUE)
) AS p (
    product_code,
    product_name,
    category_name,
    division_name,
    standard_cost,
    list_price,
    launch_date,
    is_active
)
JOIN dim_division d
    ON d.division_name = p.division_name
ON CONFLICT (product_code) DO NOTHING;