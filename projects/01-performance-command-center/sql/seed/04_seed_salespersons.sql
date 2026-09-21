-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Seed Salesperson Dimension
-- ============================================================

INSERT INTO dim_salesperson (
    salesperson_code,
    salesperson_name,
    region_id,
    channel_id,
    hire_date,
    is_active
)
SELECT
    s.salesperson_code,
    s.salesperson_name,
    r.region_id,
    ch.channel_id,
    s.hire_date,
    s.is_active
FROM (
    VALUES
        ('SP-001', 'Amelia Carter', 'Europe', 'Retail', DATE '2021-03-15', TRUE),
        ('SP-002', 'Oliver Bennett', 'Europe', 'E-commerce', DATE '2022-06-01', TRUE),
        ('SP-003', 'Sofia Laurent', 'Europe', 'Distributors', DATE '2020-09-21', TRUE),
        ('SP-004', 'Lukas Schneider', 'Europe', 'Specialty', DATE '2023-01-09', TRUE),

        ('SP-005', 'Maya Johnson', 'North America', 'Retail', DATE '2021-07-12', TRUE),
        ('SP-006', 'Ethan Williams', 'North America', 'E-commerce', DATE '2022-02-28', TRUE),
        ('SP-007', 'Isabella Martinez', 'North America', 'Distributors', DATE '2023-04-17', TRUE),
        ('SP-008', 'Daniel Brooks', 'North America', 'Direct-to-Consumer', DATE '2024-01-08', TRUE),

        ('SP-009', 'Priya Sharma', 'Emerging Markets', 'Retail', DATE '2022-08-22', TRUE),
        ('SP-010', 'Rafael Costa', 'Emerging Markets', 'Distributors', DATE '2021-11-01', TRUE),
        ('SP-011', 'Amina Khan', 'Emerging Markets', 'E-commerce', DATE '2024-03-04', TRUE),
        ('SP-012', 'Thabo Mokoena', 'Emerging Markets', 'Specialty', DATE '2023-09-18', TRUE)
) AS s(
    salesperson_code,
    salesperson_name,
    region_name,
    channel_name,
    hire_date,
    is_active
)
JOIN dim_region r
    ON r.region_name = s.region_name
JOIN dim_channel ch
    ON ch.channel_name = s.channel_name
ON CONFLICT (salesperson_code) DO NOTHING;