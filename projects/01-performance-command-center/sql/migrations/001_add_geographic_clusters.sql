-- ============================================================
-- Migration: 001_add_geographic_clusters
-- Purpose:
--   Introduce a geographic hierarchy between regions and countries.
--
-- Hierarchy:
--   Global → Region → Cluster → Country
--
-- Business rationale:
--   Enables management reporting and analysis at an intermediate
--   geographic level, such as Northern Europe or South Asia.
--
-- Dependencies:
--   dim_region and dim_country must already exist and be populated.
-- ============================================================

BEGIN;

-- 1. Create the geographic cluster dimension
CREATE TABLE IF NOT EXISTS dim_cluster (
    cluster_id SERIAL PRIMARY KEY,
    region_id INTEGER NOT NULL,
    cluster_name VARCHAR(100) NOT NULL,

    CONSTRAINT uq_cluster_region_name
        UNIQUE (region_id, cluster_name),

    CONSTRAINT fk_cluster_region
        FOREIGN KEY (region_id)
        REFERENCES dim_region(region_id)
);

-- 2. Add the cluster relationship to countries
ALTER TABLE dim_country
ADD COLUMN IF NOT EXISTS cluster_id INTEGER;

-- 3. Insert management-defined geographic clusters
INSERT INTO dim_cluster (region_id, cluster_name)
SELECT r.region_id, c.cluster_name
FROM dim_region r
JOIN (
    VALUES
        ('Europe', 'Northern Europe'),
        ('Europe', 'Central Europe'),
        ('Europe', 'Southern Europe'),
        ('North America', 'US & Canada'),
        ('North America', 'Mexico'),
        ('Emerging Markets', 'Latin America'),
        ('Emerging Markets', 'South Asia'),
        ('Emerging Markets', 'Southern Africa'),
        ('Emerging Markets', 'Middle East')
) AS c(region_name, cluster_name)
    ON r.region_name = c.region_name
ON CONFLICT (region_id, cluster_name) DO NOTHING;

-- 4. Assign countries to their clusters
UPDATE dim_country
SET cluster_id = dc.cluster_id
FROM dim_cluster dc
JOIN dim_region r
    ON dc.region_id = r.region_id
WHERE
    (
        r.region_name = 'Europe'
        AND dc.cluster_name = 'Northern Europe'
        AND country_name IN ('United Kingdom', 'Netherlands')
    )
    OR
    (
        r.region_name = 'Europe'
        AND dc.cluster_name = 'Central Europe'
        AND country_name = 'Germany'
    )
    OR
    (
        r.region_name = 'Europe'
        AND dc.cluster_name = 'Southern Europe'
        AND country_name IN ('France', 'Spain', 'Italy')
    )
    OR
    (
        r.region_name = 'North America'
        AND dc.cluster_name = 'US & Canada'
        AND country_name IN ('United States', 'Canada')
    )
    OR
    (
        r.region_name = 'North America'
        AND dc.cluster_name = 'Mexico'
        AND country_name = 'Mexico'
    )
    OR
    (
        r.region_name = 'Emerging Markets'
        AND dc.cluster_name = 'Latin America'
        AND country_name = 'Brazil'
    )
    OR
    (
        r.region_name = 'Emerging Markets'
        AND dc.cluster_name = 'South Asia'
        AND country_name = 'India'
    )
    OR
    (
        r.region_name = 'Emerging Markets'
        AND dc.cluster_name = 'Southern Africa'
        AND country_name = 'South Africa'
    )
    OR
    (
        r.region_name = 'Emerging Markets'
        AND dc.cluster_name = 'Middle East'
        AND country_name = 'United Arab Emirates'
    );

-- 5. Add the foreign key only if it does not already exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_country_cluster'
    ) THEN
        ALTER TABLE dim_country
        ADD CONSTRAINT fk_country_cluster
        FOREIGN KEY (cluster_id)
        REFERENCES dim_cluster(cluster_id);
    END IF;
END $$;

-- 6. Confirm that every country has a cluster assignment
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM dim_country
        WHERE cluster_id IS NULL
    ) THEN
        RAISE EXCEPTION
            'Migration stopped: one or more countries have no cluster assignment.';
    END IF;
END $$;

-- 7. Make cluster assignment mandatory
ALTER TABLE dim_country
ALTER COLUMN cluster_id SET NOT NULL;

COMMIT;