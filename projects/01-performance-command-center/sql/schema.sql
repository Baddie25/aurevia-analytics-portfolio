
-- ============================================================
-- Aurevia Group — Project 1 Database Schema
-- Enterprise Performance Command Center
-- ============================================================

-- Dimension tables
-- Purpose: describe the business entities used in analysis.

-- 1. Date dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key        INTEGER PRIMARY KEY,
    full_date       DATE NOT NULL UNIQUE,
    year            INTEGER NOT NULL,
    quarter         INTEGER NOT NULL,
    month           INTEGER NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    week_of_year    INTEGER NOT NULL
);

-- 2. Division dimension
CREATE TABLE IF NOT EXISTS dim_division (
    division_id     SERIAL PRIMARY KEY,
    division_name   VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Region dimension
CREATE TABLE IF NOT EXISTS dim_region (
    region_id       SERIAL PRIMARY KEY,
    region_name     VARCHAR(100) NOT NULL UNIQUE
);

-- 4. Country dimension
CREATE TABLE IF NOT EXISTS dim_country (
    country_id      SERIAL PRIMARY KEY,
    country_name    VARCHAR(100) NOT NULL UNIQUE,
    country_code    CHAR(2) NOT NULL UNIQUE,
    region_id       INTEGER NOT NULL
        REFERENCES dim_region(region_id)
);

-- 5. Channel dimension
CREATE TABLE IF NOT EXISTS dim_channel (
    channel_id      SERIAL PRIMARY KEY,
    channel_name    VARCHAR(100) NOT NULL UNIQUE
);

-- 6. Customer dimension
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id     SERIAL PRIMARY KEY,
    customer_code   VARCHAR(30) NOT NULL UNIQUE,
    customer_name   VARCHAR(150) NOT NULL,
    customer_type   VARCHAR(50) NOT NULL,
    country_id      INTEGER NOT NULL
        REFERENCES dim_country(country_id),
    channel_id      INTEGER NOT NULL
        REFERENCES dim_channel(channel_id),
    customer_segment VARCHAR(50),
    acquisition_date DATE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

-- 7. Product dimension
CREATE TABLE IF NOT EXISTS dim_product (
    product_id      SERIAL PRIMARY KEY,
    product_code    VARCHAR(30) NOT NULL UNIQUE,
    product_name    VARCHAR(150) NOT NULL,
    category_name   VARCHAR(100) NOT NULL,
    division_id     INTEGER NOT NULL
        REFERENCES dim_division(division_id),
    standard_cost   NUMERIC(12,2) NOT NULL
        CHECK (standard_cost >= 0),
    list_price      NUMERIC(12,2) NOT NULL
        CHECK (list_price >= 0),
    launch_date     DATE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

-- 8. Salesperson dimension
CREATE TABLE IF NOT EXISTS dim_salesperson (
    salesperson_id  SERIAL PRIMARY KEY,
    salesperson_code VARCHAR(30) NOT NULL UNIQUE,
    salesperson_name VARCHAR(150) NOT NULL,
    region_id        INTEGER REFERENCES dim_region(region_id),
    channel_id       INTEGER REFERENCES dim_channel(channel_id),
    hire_date        DATE,
    is_active        BOOLEAN NOT NULL DEFAULT TRUE
);



-- ============================================================
-- FACT TABLES
-- Purpose: store measurable business transactions and targets.
-- ============================================================

-- 9. Sales fact table
-- Grain: one product line within one customer order.

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id        BIGSERIAL PRIMARY KEY,
    order_id        VARCHAR(40) NOT NULL,
    order_line_number INTEGER NOT NULL,

    order_date      DATE NOT NULL
        REFERENCES dim_date(full_date),

    customer_id     INTEGER NOT NULL
        REFERENCES dim_customer(customer_id),

    product_id      INTEGER NOT NULL
        REFERENCES dim_product(product_id),

    salesperson_id  INTEGER
        REFERENCES dim_salesperson(salesperson_id),

    quantity        INTEGER NOT NULL
        CHECK (quantity > 0),

    unit_list_price NUMERIC(12,2) NOT NULL
        CHECK (unit_list_price >= 0),

    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0
        CHECK (discount_amount >= 0),

    unit_cost       NUMERIC(12,2) NOT NULL
        CHECK (unit_cost >= 0),

    gross_sales_amount NUMERIC(14,2) NOT NULL
        CHECK (gross_sales_amount >= 0),

    net_sales_amount NUMERIC(14,2) NOT NULL
        CHECK (net_sales_amount >= 0),

    product_cost_amount NUMERIC(14,2) NOT NULL
        CHECK (product_cost_amount >= 0),

    gross_profit_amount NUMERIC(14,2) NOT NULL,

    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_sales_order_line
        UNIQUE (order_id, order_line_number),

    CONSTRAINT chk_sales_discount
        CHECK (discount_amount <= gross_sales_amount),

    CONSTRAINT chk_sales_net_amount
        CHECK (net_sales_amount <= gross_sales_amount)
);


-- 10. Returns fact table
-- Grain: one returned product line associated with an order.

CREATE TABLE IF NOT EXISTS fact_returns (
    return_id       BIGSERIAL PRIMARY KEY,

    order_id        VARCHAR(40) NOT NULL,

    sales_id        BIGINT
        REFERENCES fact_sales(sales_id),

    return_date     DATE NOT NULL
        REFERENCES dim_date(full_date),

    customer_id     INTEGER NOT NULL
        REFERENCES dim_customer(customer_id),

    product_id      INTEGER NOT NULL
        REFERENCES dim_product(product_id),

    returned_quantity INTEGER NOT NULL
        CHECK (returned_quantity > 0),

    return_reason   VARCHAR(100),

    refund_amount   NUMERIC(14,2) NOT NULL
        CHECK (refund_amount >= 0),

    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- 11. Targets fact table
-- Grain: one target record for a date, division, region, and channel.

CREATE TABLE IF NOT EXISTS fact_targets (
    target_id       BIGSERIAL PRIMARY KEY,

    target_date     DATE NOT NULL
        REFERENCES dim_date(full_date),

    division_id     INTEGER NOT NULL
        REFERENCES dim_division(division_id),

    region_id       INTEGER NOT NULL
        REFERENCES dim_region(region_id),

    channel_id      INTEGER NOT NULL
        REFERENCES dim_channel(channel_id),

    revenue_target  NUMERIC(14,2) NOT NULL
        CHECK (revenue_target >= 0),

    gross_profit_target NUMERIC(14,2) NOT NULL
        CHECK (gross_profit_target >= 0),

    order_target    INTEGER NOT NULL
        CHECK (order_target >= 0),

    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_target_dimension
        UNIQUE (
            target_date,
            division_id,
            region_id,
            channel_id
        )
);