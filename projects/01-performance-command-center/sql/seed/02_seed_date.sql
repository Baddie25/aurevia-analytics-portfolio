-- ============================================================
-- AUREVIA GROUP
-- Project 1: Enterprise Performance Command Center
-- Seed date dimension
-- ============================================================

INSERT INTO dim_date (
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    week_of_year
)

SELECT
    TO_CHAR(date_value, 'YYYYMMDD')::INTEGER AS date_key,
    date_value::DATE AS full_date,
    EXTRACT(YEAR FROM date_value)::INTEGER AS year,
    EXTRACT(QUARTER FROM date_value)::INTEGER AS quarter,
    EXTRACT(MONTH FROM date_value)::INTEGER AS month,
    TO_CHAR(date_value, 'Month') AS month_name,
    EXTRACT(WEEK FROM date_value)::INTEGER AS week_of_year

FROM GENERATE_SERIES(
    DATE '2022-01-01',
    DATE '2026-12-31',
    INTERVAL '1 day'
) AS date_series(date_value)

ON CONFLICT (date_key) DO NOTHING;