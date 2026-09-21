
-- ============================================================
-- Aurevia Group
-- Project 1: Enterprise Performance Command Center
-- Seed Customer Dimension
-- ============================================================

INSERT INTO dim_customer (
    customer_code,
    customer_name,
    customer_type,
    country_id,
    channel_id,
    customer_segment,
    acquisition_date,
    is_active
)
SELECT
    s.customer_code,
    s.customer_name,
    s.customer_type,
    co.country_id,
    ch.channel_id,
    s.customer_segment,
    s.acquisition_date,
    s.is_active
FROM (
    VALUES
        ('CU-001', 'Northstar Retail Group', 'Retail Chain', 'United Kingdom', 'Retail', 'Strategic', DATE '2022-01-15', TRUE),
        ('CU-002', 'Horizon Home Stores', 'Retail Chain', 'Germany', 'Retail', 'Core', DATE '2022-04-20', TRUE),
        ('CU-003', 'Maison & Vie', 'Retail Chain', 'France', 'Retail', 'Growth', DATE '2023-02-10', TRUE),
        ('CU-004', 'EuroValue Market', 'Retail Chain', 'Netherlands', 'Retail', 'Core', DATE '2022-08-05', TRUE),
        ('CU-005', 'Iberia Essentials', 'Retail Chain', 'Spain', 'Retail', 'Growth', DATE '2023-06-12', TRUE),
        ('CU-006', 'Italia Living', 'Retail Chain', 'Italy', 'Specialty', 'Core', DATE '2022-11-18', TRUE),

        ('CU-007', 'Atlantic Commerce', 'E-commerce Marketplace', 'United States', 'E-commerce', 'Strategic', DATE '2023-01-09', TRUE),
        ('CU-008', 'Maple Digital Market', 'E-commerce Marketplace', 'Canada', 'E-commerce', 'Growth', DATE '2023-04-14', TRUE),
        ('CU-009', 'Pacific Wellness Online', 'E-commerce Marketplace', 'United States', 'E-commerce', 'Growth', DATE '2024-02-22', TRUE),
        ('CU-010', 'Mexico Value Online', 'E-commerce Marketplace', 'Mexico', 'E-commerce', 'Emerging', DATE '2024-05-16', TRUE),

        ('CU-011', 'GlobalCare Distribution', 'Distributor', 'United Kingdom', 'Distributors', 'Strategic', DATE '2022-03-11', TRUE),
        ('CU-012', 'Central Trade Partners', 'Distributor', 'Germany', 'Distributors', 'Core', DATE '2022-07-19', TRUE),
        ('CU-013', 'Andes Consumer Supply', 'Distributor', 'Brazil', 'Distributors', 'Emerging', DATE '2024-01-17', TRUE),
        ('CU-014', 'India Market Link', 'Distributor', 'India', 'Distributors', 'Growth', DATE '2023-09-23', TRUE),
        ('CU-015', 'Africa Retail Supply', 'Distributor', 'South Africa', 'Distributors', 'Emerging', DATE '2024-03-08', TRUE),

        ('CU-016', 'Aurevia Online Store UK', 'Direct Consumer', 'United Kingdom', 'Direct-to-Consumer', 'Growth', DATE '2023-01-01', TRUE),
        ('CU-017', 'Aurevia Online Store US', 'Direct Consumer', 'United States', 'Direct-to-Consumer', 'Strategic', DATE '2023-05-10', TRUE),
        ('CU-018', 'Aurevia Online Store Germany', 'Direct Consumer', 'Germany', 'Direct-to-Consumer', 'Growth', DATE '2024-01-12', TRUE),
        ('CU-019', 'Wellness Boutique London', 'Specialty Retailer', 'United Kingdom', 'Specialty', 'Core', DATE '2022-09-14', TRUE),
        ('CU-020', 'Urban Health Collective', 'Specialty Retailer', 'France', 'Specialty', 'Growth', DATE '2023-11-06', TRUE),

        ('CU-021', 'Gulf Lifestyle Partners', 'Distributor', 'United Arab Emirates', 'Distributors', 'Emerging', DATE '2024-06-21', TRUE),
        ('CU-022', 'Southern Wellness Stores', 'Retail Chain', 'South Africa', 'Retail', 'Emerging', DATE '2024-04-03', TRUE),
        ('CU-023', 'Brazil Home Network', 'Retail Chain', 'Brazil', 'Retail', 'Growth', DATE '2023-08-15', TRUE),
        ('CU-024', 'India Everyday Retail', 'Retail Chain', 'India', 'Retail', 'Growth', DATE '2024-02-05', TRUE)
) AS s (
    customer_code,
    customer_name,
    customer_type,
    country_name,
    channel_name,
    customer_segment,
    acquisition_date,
    is_active
)
JOIN dim_country co
    ON co.country_name = s.country_name
JOIN dim_channel ch
    ON ch.channel_name = s.channel_name
ON CONFLICT (customer_code) DO NOTHING;