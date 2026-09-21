-- ============================================================
-- AUREVIA GROUP
-- Project 1: Enterprise Performance Command Center
-- Seed foundational dimension data
-- ============================================================

-- 1. Business divisions
INSERT INTO dim_division (division_id, division_name)
VALUES
    (1, 'Personal Care'),
    (2, 'Home & Lifestyle'),
    (3, 'Wellness'),
    (4, 'Everyday Essentials');


-- 2. Geographic regions
INSERT INTO dim_region (region_id, region_name)
VALUES
    (1, 'Europe'),
    (2, 'North America'),
    (3, 'Emerging Markets');


-- 3. Countries

INSERT INTO dim_country (
    country_id,
    country_name,
    country_code,
    region_id
)

VALUES
    (1, 'United Kingdom', 'GB', 1),
    (2, 'Germany', 'DE', 1),
    (3, 'France', 'FR', 1),
    (4, 'Netherlands', 'NL', 1),
    (5, 'Spain', 'ES', 1),
    (6, 'Italy', 'IT', 1),
    (7, 'United States', 'US', 2),
    (8, 'Canada', 'CA', 2),
    (9, 'Mexico', 'MX', 2),
    (10, 'Brazil', 'BR', 3),
    (11, 'India', 'IN', 3),
    (12, 'South Africa', 'ZA', 3),
    (13, 'United Arab Emirates', 'AE', 3);


-- 4. Sales channels
INSERT INTO dim_channel (channel_id, channel_name)
VALUES
    (1, 'Retail'),
    (2, 'E-commerce'),
    (3, 'Distributors'),
    (4, 'Direct-to-Consumer'),
    (5, 'Specialty');