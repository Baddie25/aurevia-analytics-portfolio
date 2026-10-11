# Aurevia Group — Enterprise Performance Command Center

> **Portfolio Project 1 | Enterprise Performance Management, Business Intelligence & Executive Decision Support**

**Status:** Core SQL analysis, target/variance analysis, validation, and executive reporting completed. Power BI dashboard pending.

---

## 1. Project Overview

The Enterprise Performance Command Center is a business intelligence and enterprise performance management project designed to help the leadership team of Aurevia Group understand enterprise performance, identify commercial risks, evaluate performance against management benchmarks, and prioritise management action.

Aurevia Group is a **fictional global consumer and retail company headquartered in London**, operating across Personal Care, Home & Lifestyle, Wellness, and Everyday Essentials. Its geographic markets include Europe, North America, and Emerging Markets.

This project establishes a structured analytical foundation for executive reporting by integrating sales, product, customer, geographic, channel, returns, and target data into a relational database and a collection of SQL analyses.

The project follows an end-to-end analytical workflow:

**Business problem → Data model → Performance measurement → SQL analytics → Validation → Target/variance analysis → Executive reporting → Management decisions**

The project therefore extends beyond historical reporting. It establishes a performance-management framework in which actual business performance can be measured consistently, compared with defined benchmarks, investigated through variance analysis, and translated into management questions and recommended actions.

The Power BI dashboard is planned but remains on hold until suitable access to Power BI is available.

> **Data transparency:** Aurevia Group and the company dataset are fictional and simulated for portfolio purposes. The results demonstrate analytical methods, performance management, and decision-making; they are not claims about the performance of a real company.

---

## 2. Business Problem

Senior leaders need a consistent view of business performance across products, divisions, customers, sales channels, and geographic markets.

Without a reliable analytical framework, management may struggle to distinguish sustainable growth from changes in sales mix, understand where profit is concentrated, assess discounting, identify return-related issues, or determine whether actual performance is meeting defined expectations.

This project addresses the following management questions:

- How has revenue evolved over the reporting period?
- Is gross profitability stable?
- Which sales channels contribute the most revenue?
- How concentrated are revenue and gross profit among products and customers?
- How much revenue is given up through discounts?
- What proportion of sold units is returned, and what is the associated refund and estimated gross-profit impact?
- How does actual performance compare with the defined revenue, gross-profit, and order benchmarks?
- Where are the largest positive and negative variances?
- Which findings warrant further commercial investigation or management action?

The purpose is not simply to report historical results. It is to translate business data into evidence that can support better decisions and provide a repeatable foundation for enterprise performance management.

---

## 3. Project Objectives

The project aims to:

1. Build a relational PostgreSQL data model for enterprise commercial and performance reporting.

2. Integrate sales, returns, customer, product, division, channel, geographic, and target dimensions.

3. Develop reusable SQL analyses for key performance indicators and supporting metrics.

4. Establish consistent performance definitions for revenue, gross profit, margin, discounts, returns, and related measures.

5. Validate calculations and avoid common aggregation errors.

6. Compare actual performance with defined revenue, gross-profit, and order benchmarks.

7. Identify performance patterns, concentration risks, variances, and opportunities for further investigation.

8. Translate analytical findings into executive-level reporting, management questions, and recommendations.

9. Establish a reproducible analytical foundation for a future Power BI dashboard.

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational database, data model, validation, and analytical queries |
| SQL | Data modelling, aggregation, joins, KPI calculation, target/variance analysis, and validation |
| Git and GitHub | Version control and portfolio project history |
| Visual Studio Code | SQL development, documentation, and project organisation |
| Power BI | Planned interactive performance-management dashboard; currently pending |

Python is available in the wider portfolio environment, but the core findings documented here are based on the SQL analysis and validated results.

---

## 5. Data Model and Methodology

### 5.1 Database design

The database uses a dimensional model with descriptive dimension tables and measurable fact tables.

The schema includes dimensions for:

- Date
- Division
- Region
- Country
- Geographic cluster, introduced through a migration
- Sales channel
- Customer
- Product
- Salesperson

TThe principal fact tables include:

- `fact_sales` — sales transactions at product-order-line level
- `fact_returns` — returned product lines associated with original sales orders
- `fact_targets` — illustrative performance benchmarks recorded by date, division, region, and channel

The sales fact table records transaction measures including quantity, unit list price, discount amount, unit cost, gross sales, net sales, product cost, and gross profit.

The returns fact table records returned quantity, return date, return reason, and refund amount for returned sales lines.

The targets fact table records:

- Revenue target
- Gross-profit target
- Order target

at the defined target grain of date, division, region, and channel.

Primary keys, foreign keys, uniqueness constraints, and non-negative value checks are used to support referential integrity and data quality.

The target table uses a composite uniqueness rule across:

**Target date × Division × Region × Channel**

This prevents duplicate target records at the defined planning grain.

### 5.2 Geographic hierarchy

A database migration introduces geographic clusters between regions and countries:

**Global → Region → Cluster → Country**

This enables reporting at a more useful management level than country or region alone.

The migration creates the cluster dimension, assigns countries to management-defined clusters, adds the relevant relationship to the country dimension, and validates that countries have cluster assignments.

### 5.3 Analytical workflow

The analytical process includes:

1. Creating the database schema.
2. Seeding dimension and transaction data.
3. Applying the geographic-cluster migration.
4. Seeding the illustrative performance benchmarks.
5. Querying the data at the appropriate business grain.
6. Aggregating sales and returns separately where necessary.
7. Calculating KPIs and supporting metrics.
8. Comparing actual results with defined benchmarks.
9. Validating totals, joins, target coverage, and derived measures.
10. Translating findings into executive reporting and management recommendations.

The analytical approach deliberately separates **measurement** from **interpretation**.

The SQL layer establishes what happened in the simulated dataset. The executive layer then considers what those results may mean for management, while avoiding unsupported causal claims.

### 5.4 Returns calculation and aggregation control

Sales transactions and return activity are represented within `fact_sales`. For analytical purposes, return activity is aggregated separately from sales measures where necessary before the results are compared.

The reported unit return rate is calculated as:

**Returned units ÷ Units sold × 100**

Returns are attributed to the original sale month for cohort analysis rather than automatically being assigned to the month in which the return was processed.

The estimated gross-profit impact is a derived analytical measure. It should not be interpreted as a fully reconciled accounting adjustment.

### 5.5 Target and variance methodology

The project includes a target-versus-actual analytical extension using `fact_targets`.

The current target dataset is **synthetic and illustrative**. It was created because Aurevia Group is a fictional company and therefore has no genuine historical management budget or approved operating plan from which real targets could be sourced.

The current benchmark methodology uses a transparent planning assumption:

- Revenue target = simulated actual baseline × 1.05
- Gross-profit target = simulated actual baseline × 1.05
- Order target = simulated actual order baseline × 1.05, rounded upward

These targets should therefore be understood as **illustrative planning benchmarks**, not historical management targets, approved budgets, forecasts, or externally validated business expectations.

The purpose of this methodology is to demonstrate the mechanics of performance management:

**Actual → Target → Variance → Management investigation**

It is not intended to claim that a uniform 5% uplift represents conventional corporate target-setting practice.

In a real organisation, target setting would normally incorporate factors such as:

- Strategic objectives
- Prior-period performance
- Market growth assumptions
- Pricing and volume expectations
- Product and channel strategy
- Operational capacity
- Geographic priorities
- Cost and margin requirements
- External economic and competitive conditions
- Bottom-up business-unit plans
- Management ambition and governance

The current Aurevia implementation therefore demonstrates the **analytical framework for target and variance management**, while explicitly acknowledging that the target-setting methodology itself is illustrative.

### 5.6 Target data quality and join control

The target framework was validated for:

- Target record count
- Target uniqueness
- Target date coverage
- Positive revenue targets
- Positive gross-profit targets
- Positive order targets
- Alignment between target months and sales months
- Successful execution of the target-versus-actual query

The target dataset contains **1,257 target records** covering **48 months from January 2022 through December 2025**.

All 48 target months have corresponding sales activity.

The target-versus-actual analysis aggregates actual performance to the same management grain as the targets before joining the datasets.

This is important because joining targets to lower-grain actual data can create fanout and artificially inflate actual or target values.

The validated target-versus-actual query therefore operates at:

**Month × Division × Region × Channel**

rather than introducing unnecessary country-level detail into the target join.

---

## 6. Key Findings

The following results are based on the current simulated dataset for 2022–2025.

### 6.1 Enterprise performance

| KPI / Metric | Result |
|---|---:|
| Net revenue | £182,967.68 |
| Gross revenue before discounts | £191,888.18 |
| Discounts | £8,920.50 |
| Product cost | £68,722.70 |
| Gross profit | £114,244.98 |
| Gross margin | 62.44% |
| Enterprise discount rate | 4.65% |

Gross profit is calculated as net revenue less product cost.

Gross margin is gross profit divided by net revenue.

The discount rate is calculated as total discounts divided by gross revenue before discounts.

These definitions provide the core enterprise performance measures used throughout the project.

### 6.2 Annual net revenue

| Year | Net Revenue |
|---|---:|
| 2022 | £47,770.47 |
| 2023 | £45,632.27 |
| 2024 | £44,587.92 |
| 2025 | £44,977.02 |
| **Total** | **£182,967.68** |

Revenue declined after 2022, before recording a modest recovery in 2025.

This pattern warrants further investigation into volume, pricing, customer demand, channel mix, and product performance before attributing the movement to a specific cause.

Gross margin remained within a narrow range of approximately 62.40%–62.50% across the reporting years.

This indicates relative stability in the recorded gross margin despite changes in annual revenue.

The combination of revenue movement and relatively stable gross margin is therefore more informative than either metric viewed independently.

### 6.3 Revenue by sales channel

| Sales Channel | Net Revenue |
|---|---:|
| Retail | £65,542.37 |
| Distributors | £44,300.12 |
| E-commerce | £26,999.14 |
| Specialty | £23,804.87 |
| Direct-to-Consumer | £22,321.18 |

Retail is the largest recorded revenue channel, followed by distributors.

These channels merit particular attention in commercial planning because their performance has a material influence on total revenue.

Channel revenue alone does not establish channel profitability.

Further analysis should incorporate channel-specific costs, customer acquisition costs, fulfilment costs, and other relevant operating expenses before investment decisions are made.

### 6.4 Product concentration

- The top five products by net revenue account for approximately **71.7% of net revenue**.
- The top three products by net revenue account for approximately **45.8% of net revenue**.
- The top five products by gross profit contribute approximately **66.4% of gross profit**.

This concentration means enterprise results are materially influenced by a relatively small number of products.

Management should investigate the durability of demand for these products, their supply continuity, pricing power, and the potential consequences of a product-specific disruption.

Product concentration should be assessed alongside product-level growth and margin, rather than treated as inherently negative.

### 6.5 Customer concentration

The five largest customers by net revenue are:

| Customer | Approximate Share of Net Revenue |
|---|---:|
| Maison & Vie | 11.00% |
| Wellness Boutique London | 9.41% |
| Aurevia Online Store UK | 9.16% |
| India Market Link | 8.69% |
| India Everyday Retail | 6.34% |

Together, these five customers contribute approximately **44.6% of net revenue**.

This creates a potential customer-concentration exposure.

A material reduction in purchasing by one of these customers could affect enterprise results.

The next analytical step would be to assess customer retention, growth, margin contribution, payment behaviour, contract terms, and the feasibility of diversifying revenue.

### 6.6 Discounting

The enterprise discount rate is approximately **4.65%**.

Recorded discount rates by division are:

| Division | Discount Rate |
|---|---:|
| Wellness | 4.96% |
| Personal Care | 4.96% |
| Everyday Essentials | 4.35% |
| Home & Lifestyle | 4.29% |

Recorded discount rates by channel are:

| Channel | Discount Rate |
|---|---:|
| Distributors | 4.77% |
| Retail | 4.69% |
| E-commerce | 4.64% |
| Specialty | 4.55% |
| Direct-to-Consumer | 4.40% |

The differences provide a basis for further investigation into pricing discipline, channel terms, promotional effectiveness, and discount governance.

A higher discount rate does not automatically imply poor performance.

Its commercial value depends on the additional volume or customer value generated and the resulting contribution to profit.

### 6.7 Returns

| KPI / Metric | Result |
|---|---:|
| Units sold | 13,504 |
| Units returned | 237 |
| Unit return rate | 1.76% |
| Refund amount | £3,221.87 |
| Estimated gross-profit impact | £2,004.67 |

The overall unit return rate is approximately **1.76%**.

Regional return rates are:

| Region | Unit Return Rate |
|---|---:|
| Europe | 1.90% |
| Emerging Markets | 1.63% |
| North America | 1.56% |

The highest recorded country-level return rates include:

| Country | Unit Return Rate |
|---|---:|
| Italy | 3.00% |
| Spain | 2.79% |
| Germany | 2.14% |

These differences warrant investigation into return reasons, product quality, customer expectations, fulfilment, and country-specific operating conditions.

The available figures identify where to investigate; they do not establish the cause of returns.

The estimated gross-profit impact is a derived estimate, not a substitute for a finance-approved returns accounting treatment.

### 6.8 Target versus actual performance

The target framework contains **1,257 target records across 48 months**, covering January 2022 through December 2025.

The targets are deliberately constructed as illustrative planning benchmarks based on a 5% uplift over the simulated actual baseline.

The resulting enterprise-level target totals are:

| Target Measure | Illustrative Target |
|---|---:|
| Revenue target | £192,116.57 |
| Gross-profit target | £119,957.85 |
| Order target | 4,257 |

Because the targets are constructed from the simulated historical actual baseline, the resulting variances should **not** be interpreted as evidence that Aurevia historically underperformed an independently established management plan.

This is an important analytical distinction.

The target analysis demonstrates the mechanics of performance management rather than providing an independent assessment of historical target attainment.

At the analytical level, the SQL framework compares:

- Actual revenue vs revenue target
- Actual gross profit vs gross-profit target
- Actual order count vs order target
- Absolute variance
- Percentage variance

The analysis is performed at:

**Month × Division × Region × Channel**

This creates a management-oriented variance framework that can later be connected to a more realistic target-setting methodology.

A future version of the project could replace or supplement the illustrative benchmark with a driver-based management plan incorporating strategic growth assumptions, market conditions, pricing, volume, margin, channel priorities, and operational capacity.

---

## 7. Executive Implications and Recommended Actions

The analysis supports six areas for management attention.

### 7.1 Investigate the revenue trajectory

Revenue declined between 2022 and 2024 before recovering modestly in 2025.

**Recommended action:** Decompose the change into price, volume, product mix, channel mix, and customer-level drivers before setting growth interventions.

### 7.2 Protect concentrated sources of value

A substantial share of revenue and gross profit comes from a small number of customers and products.

**Recommended action:** Develop a concentration-risk review covering customer retention, product continuity, alternative suppliers where relevant, and diversification opportunities.

### 7.3 Improve pricing and discount governance

Discount rates vary across divisions and channels.

**Recommended action:** Assess whether discount differences are supported by incremental volume, strategic account value, or improved customer retention. Establish clear approval thresholds and measure outcomes against margin and revenue objectives.

### 7.4 Investigate return-rate differences

Return rates vary by geography, with Italy and Spain showing relatively high recorded rates.

**Recommended action:** Analyse return reasons, affected products, sales cohorts, and operational processes before implementing targeted corrective actions.

### 7.5 Strengthen performance monitoring

The SQL model provides a foundation for consistent reporting across the enterprise.

**Recommended action:** Complete the planned Power BI dashboard when access is available, using agreed metric definitions and validated SQL outputs as the reporting baseline.

### 7.6 Mature the target and variance-management framework

The project now demonstrates how actual performance can be compared with defined management benchmarks.

However, the current targets are illustrative rather than independently derived management plans.

**Recommended action:** Treat the current target model as a proof of concept for variance analysis, then develop a more realistic driver-based target framework incorporating strategic objectives, operational drivers, market assumptions, pricing, volume, margin, channel priorities, and management expectations.

This would allow future versions of the Command Center to progress from:

**Historical performance reporting → Actual vs benchmark → Driver-based target setting → Variance diagnosis → Management action**

These are evidence-led recommendations for further investigation and decision-making.

The simulated dataset does not, by itself, prove causality or quantify the financial benefit of the proposed actions.

---

## 8. Project Structure

```text
projects/
└── 01-performance-command-center/
    ├── README.md
    ├── business-case.md
    ├── analysis/
    │   └── sql/
    │       ├── 01_yearly_performance.sql
    │       ├── 02_division_channel_performance.sql
    │       ├── 03_geographic_performance.sql
    │       ├── 04_product_performance.sql
    │       ├── 05_customer_performance.sql
    │       ├── 06_discount_performance.sql
    │       ├── 07_profitability_performance.sql
    │       ├── 08_returns_performance.sql
    │       └── 09_target_vs_actual.sql
    ├── dashboard/
    ├── executive-brief/
    │   ├── executive-brief.md
    │   └── evidence-matrix.md
    └── sql/
        ├── schema.sql
        ├── migrations/
        │   └── 001_add_geographic_clusters.sql
        └── seed/
            ├── 01_seed_dimensions.sql
            ├── 02_seed_date.sql
            ├── 03_seed_products.sql
            ├── 04_seed_salespersons.sql
            ├── 05_seed_customers.sql
            ├── 06_seed_sales.sql
            ├── 07_seed_returns.sql
            └── 08_seed_targets.sql
```

The SQL analysis directory contains the project's complete analytical query set, covering enterprise performance, division and channel performance, geographic performance, product and customer analysis, discounting, profitability, returns, and target-versus-actual performance.

---

## 9. Reproducing the Analysis

The project is designed to be reproducible in a PostgreSQL environment using the schema, seed scripts, geographic-cluster migration, target seed, and analytical SQL files included in the repository.

The reproduction workflow follows the same sequence used during development:

**Schema creation → Dimension seeding → Date seeding → Product and salesperson seeding → Customer seeding → Sales seeding → Returns seeding → Target seeding → Geographic hierarchy migration → Analytical SQL execution → Validation**

### Prerequisites

- PostgreSQL
- A PostgreSQL role with permission to create and populate the project database
- A database for the portfolio project
- A terminal, such as the integrated terminal in Visual Studio Code

The examples below assume the database is named `portfolio_db` and the PostgreSQL role is `portfolio_user`, matching the current local setup. Adapt these values if using a different environment.

**Security:** Do not put database passwords in SQL files, shell commands, README documentation, or Git commits. Use a secure local authentication method or an ignored environment file.

### Step 1 — Create or select the database

Create the database using your normal PostgreSQL administration workflow if it does not already exist.

### Step 2 — Create the schema

From the portfolio repository root, run the following commands in the **shell terminal**, not inside the PostgreSQL interactive prompt:

```bash
psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/schema.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/01_seed_dimensions.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/02_seed_date.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/03_seed_products.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/04_seed_salespersons.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/05_seed_customers.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/06_seed_sales.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/07_seed_returns.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/seed/08_seed_targets.sql

psql -d portfolio_db -U portfolio_user -v ON_ERROR_STOP=1 -f projects/01-performance-command-center/sql/migrations/001_add_geographic_clusters.sql
```

The scripts should be executed in the order shown because later scripts depend on tables and records created by earlier scripts.

The target seed is intentionally executed after the sales data is available because the current illustrative target framework derives its benchmark baseline from the simulated sales data.

### Step 3 — Verify the database structure

The schema contains the project's analytical dimensions, transactional facts, and planning-target table.

The principal tables are:

- `dim_date`
- `dim_division`
- `dim_region`
- `dim_cluster`
- `dim_country`
- `dim_channel`
- `dim_customer`
- `dim_product`
- `dim_salesperson`
- `fact_sales`
- `fact_returns`
- `fact_targets`

The geographic migration adds the `dim_cluster` hierarchy and assigns countries to geographic clusters.

### Step 4 — Verify the target framework

The target framework is implemented through:

```text
projects/01-performance-command-center/sql/seed/08_seed_targets.sql
```

The target seed creates monthly target records at the following grain:

```text
target month × division × region × channel
```

The target table uses a composite uniqueness rule across:

```text
target_date + division_id + region_id + channel_id
```

The current target methodology is explicitly **illustrative rather than historical**.

The simulated targets are generated as a 5% uplift over the corresponding simulated actual baseline:

- Revenue target = simulated actual revenue × 1.05
- Gross profit target = simulated actual gross profit × 1.05
- Order target = simulated actual distinct orders × 1.05, rounded upward

This methodology is used to demonstrate target-versus-actual analysis in a fictional company where no genuine management budget or approved historical targets exist.

It should not be interpreted as a conventional corporate budgeting methodology or as evidence that Aurevia Group actually used a 5% management growth target.

### Step 5 — Run the core analytical SQL

The core analytical queries are stored under:

```text
projects/01-performance-command-center/analysis/sql/
```

The current analysis sequence includes:

```text
01_yearly_performance.sql
02_division_performance.sql
03_channel_performance.sql
04_geographic_performance.sql
05_product_performance.sql
06_customer_performance.sql
07_discount_performance.sql
08_returns_performance.sql
09_target_vs_actual.sql
```

The queries progressively examine:

1. Enterprise performance over time
2. Division performance
3. Channel performance
4. Geographic performance
5. Product performance
6. Customer concentration
7. Discounting and revenue realization
8. Returns and operational exposure
9. Target-versus-actual performance

The analysis is intentionally modular so that individual analytical questions can be executed independently rather than relying on one large monolithic query.

### Step 6 — Run the target-versus-actual analysis

The target analysis is contained in:

```text
projects/01-performance-command-center/analysis/sql/09_target_vs_actual.sql
```

The query compares actual performance against the synthetic target framework at:

```text
month × division × region × channel
```

It reports:

- Actual revenue
- Revenue target
- Revenue variance
- Revenue variance percentage
- Actual gross profit
- Gross profit target
- Gross profit variance
- Gross profit variance percentage
- Actual segment-level order count
- Order target
- Order variance
- Order variance percentage

Actual sales are aggregated to the same geographic grain used by the target table before the target join is performed.

This aggregation step is important because joining country-level actuals directly to region-level targets would create a fanout problem and duplicate target records.

### Step 7 — Validate the target data

The target framework was validated after loading.

The validated target dataset contains:

| Validation Measure | Result |
|---|---:|
| Target records | 1,257 |
| Target months | 48 |
| First target month | January 2022 |
| Last target month | December 2025 |
| Non-positive revenue targets | 0 |
| Non-positive gross profit targets | 0 |
| Non-positive order targets | 0 |
| Months with sales | 48 |
| Months without sales | 0 |
| Unique target combinations | 1,257 |

The resulting target analysis contains **1,257 monthly division-region-channel combinations**.

The validation also confirmed that the target grain aligns with the intended join dimensions and that the target records do not contain duplicate combinations.

### Step 8 — Reproduce the executive analysis

After executing the SQL queries, the resulting outputs can be used to reproduce the executive findings documented in:

```text
projects/01-performance-command-center/executive-brief/executive-brief.md
```

and:

```text
projects/01-performance-command-center/executive-brief/evidence-matrix.md
```

The executive reporting layer is intentionally separated from the raw SQL layer.

The SQL establishes the analytical evidence.

The Evidence Matrix organizes the evidence around management questions.

The Executive Brief translates validated findings into management implications and decision priorities.

### Reproduction principle

The project separates:

```text
Data generation
    ↓
Data model
    ↓
SQL analysis
    ↓
Analytical validation
    ↓
Evidence synthesis
    ↓
Executive interpretation
```

This separation is deliberate. It makes the project easier to audit, reproduce, extend, and eventually connect to a Power BI semantic model.

---

## 10. Deliverables

The project produces a complete analytical and executive-decision-support package rather than a standalone collection of SQL queries.

### Core deliverables

| Deliverable | Purpose |
|---|---|
| `README.md` | Project documentation, methodology, findings, reproduction instructions, limitations, and portfolio context |
| `business-case.md` | Business problem, decision context, value proposition, and management relevance |
| `executive-brief.md` | Executive interpretation of the validated analytical findings |
| `evidence-matrix.md` | Traceability between management questions, analytical evidence, findings, and decision implications |
| `schema.sql` | PostgreSQL schema and relational data model |
| Seed scripts | Reproducible simulated dimensions, sales, returns, and target data |
| Geographic migration | Geographic cluster hierarchy and country-to-cluster assignment |
| Analytical SQL | Reproducible analytical queries supporting the project findings |
| Target-versus-actual analysis | Performance management analysis comparing actual performance with illustrative planning benchmarks |

### SQL deliverables

The analytical SQL package includes:

```text
analysis/sql/
├── 01_yearly_performance.sql
├── 02_division_performance.sql
├── 03_channel_performance.sql
├── 04_geographic_performance.sql
├── 05_product_performance.sql
├── 06_customer_performance.sql
├── 07_discount_performance.sql
├── 08_returns_performance.sql
└── 09_target_vs_actual.sql
```

These queries provide the analytical foundation for the executive reporting layer.

### Data-generation deliverables

The reproducible data-generation layer includes:

```text
sql/seed/
├── 01_seed_dimensions.sql
├── 02_seed_date.sql
├── 03_seed_products.sql
├── 04_seed_salespersons.sql
├── 05_seed_customers.sql
├── 06_seed_sales.sql
├── 07_seed_returns.sql
└── 08_seed_targets.sql
```

The target seed is included as a separate analytical component so that the performance-management layer can be distinguished from the underlying transactional sales data.

### Geographic hierarchy deliverable

The project also includes:

```text
sql/migrations/001_add_geographic_clusters.sql
```

This migration introduces the geographic cluster hierarchy used to support more meaningful regional analysis.

The hierarchy provides an additional analytical layer between country and broader region.

### Executive decision-support deliverables

The Executive Brief and Evidence Matrix translate the SQL findings into a management-oriented narrative.

The Evidence Matrix provides traceability between:

```text
Executive Question
    ↓
Analytical Evidence
    ↓
Validated Finding
    ↓
Management Interpretation
    ↓
Decision Question
```

The Executive Brief then consolidates the most material findings into an executive-level view of:

- Enterprise performance
- Growth and profitability
- Product and customer concentration
- Channel and geographic performance
- Discounting and revenue realization
- Returns exposure
- Target-versus-actual performance
- Cross-analysis
- Management priorities
- Further investigation requirements

### Power BI deliverable

The intended Power BI dashboard remains a future presentation layer.

The current project establishes the analytical foundation required for that dashboard:

- Validated relational data
- Reproducible SQL
- Defined KPIs
- Target-versus-actual structure
- Executive evidence
- Documented methodology
- Decision-oriented findings

The Power BI implementation is therefore a presentation-layer extension rather than a prerequisite for the underlying analytical work.

---

## 11. Limitations and Assumptions

This project is intentionally transparent about its limitations because the objective is to demonstrate analytical reasoning and executive decision support rather than simulate a real company's confidential internal reporting environment.

### 1. Aurevia Group is fictional

Aurevia Group is a fictional company created specifically for this portfolio.

The company, transactions, customers, products, illustrative planning benchmarks, and operational performance are simulated.

The project should therefore be evaluated as a demonstration of analytical methodology, business reasoning, and technical execution rather than as a factual representation of a real organization.

### 2. The financial data is simulated

The sales, product costs, discounts, gross profit, returns, and other operational values are synthetic.

The resulting financial metrics are internally calculated from the simulated dataset.

They should not be interpreted as real company financial results.

### 3. External market evidence is separate from Aurevia's simulated performance

Where external market information is used in the broader portfolio, it should be clearly distinguished from Aurevia's internal simulated data.

External market evidence provides contextual assumptions or strategic benchmarks.

It does not validate the simulated Aurevia financial results.

### 4. EBITDA is not reported

The current model does not contain sufficient operating-expense detail to calculate a defensible EBITDA figure.

Gross profit is therefore used as the primary profitability measure.

A future version could introduce operating expenses, logistics costs, personnel costs, marketing expenditure, and other cost categories to support a broader profitability bridge.

### 5. Target data is synthetic

The `fact_targets` framework is not historical management data.

The targets are illustrative planning benchmarks created for the portfolio.

They are currently derived from the simulated actual baseline using a transparent 5% uplift methodology.

This makes the target framework reproducible and auditable, but it also means that the resulting target variance should not be interpreted as evidence of actual historical management performance.

### 6. The current target methodology is not intended to represent best-practice corporate planning

A simple 5% uplift is useful for demonstrating target-versus-actual mechanics, but real organizations typically establish targets using a combination of:

- Historical performance
- Forecasts
- Strategic priorities
- Market growth expectations
- Pricing assumptions
- Volume assumptions
- Capacity constraints
- Margin objectives
- Regional priorities
- Product strategy
- Management ambition
- Bottom-up business-unit planning
- External market and macroeconomic evidence

A future iteration could replace or supplement the illustrative benchmark with a driver-based management target framework.

### 7. Segment-level order counts should not be interpreted as enterprise-wide unique orders

The target-versus-actual analysis operates at the:

```text
month × division × region × channel
```

grain.

Distinct orders are therefore calculated within those analytical segments.

If a single enterprise order contains multiple products or divisions, summing segment-level distinct order counts can result in the same enterprise order being represented in more than one segment.

The order metric should therefore be interpreted as a **segment-level order measure**, not automatically as a unique enterprise-wide order count.

### 8. Returns are analytically separated from sales

Returns analysis requires careful aggregation because joining transactional returns directly to sales can create duplication and distort revenue or return metrics.

The project therefore aggregates return activity separately and attributes return cohorts to the original sale month where appropriate.

Return rate is calculated using returned units relative to sold units.

Refund value is distinguished from the estimated gross-profit impact of returns.

The estimated gross-profit impact is an analytical estimate rather than a complete accounting treatment.

### 9. Power BI has not yet been implemented

The analytical foundation is complete, but the final Power BI dashboard remains pending.

Consequently, the project currently demonstrates the analytical model, SQL analysis, validation, evidence synthesis, and executive reporting layers more fully than the final interactive visualization layer.

### Overall interpretation of the limitations

These limitations do not invalidate the project.

They define the boundary between:

```text
Demonstrated analytical capability
```

and:

```text
Future production-grade enterprise implementation
```

The project intentionally favors transparency over presenting simulated data as if it were real corporate information.

---

## 12. Project Status

The project is considered analytically complete at the SQL, validation, and executive-reporting stages, with the interactive Power BI presentation layer remaining as the principal unfinished component.

| Component | Status | Description |
|---|---|---|
| Business case | Completed | Business problem, decision context, and management relevance documented |
| Data model | Completed | Relational PostgreSQL model implemented |
| Core dimensions | Completed | Organizational, geographic, product, customer, channel, and salesperson dimensions implemented |
| Sales fact | Completed | Transactional sales model populated |
| Returns analysis | Completed | Returns logic validated and incorporated into executive findings |
| Geographic clusters | Implemented | Cluster hierarchy added through migration |
| Core SQL analysis | Completed | Enterprise, division, channel, geographic, product, customer, discount, and returns analysis completed |
| Target framework | Completed | Synthetic monthly target structure implemented |
| Target seed | Completed | `08_seed_targets.sql` implemented and validated |
| Target-versus-actual SQL | Completed | `09_target_vs_actual.sql` implemented and validated |
| Target data validation | Completed | Grain, coverage, uniqueness, and positive-value checks completed |
| Executive Brief | Completed | Executive findings and implications documented |
| Evidence Matrix | Completed | Analytical evidence linked to management questions |
| README documentation | Completed | Methodology, findings, reproduction, limitations, and portfolio context documented |
| Power BI dashboard | Pending | Interactive executive presentation layer remains to be implemented |

### Current analytical status

The project currently supports a complete analytical workflow:

```text
Simulated business data
        ↓
Relational data model
        ↓
SQL analytical layer
        ↓
Performance measurement
        ↓
Target / variance analysis
        ↓
Analytical validation
        ↓
Evidence Matrix
        ↓
Executive Brief
        ↓
Management priorities
```

### Remaining work

The principal remaining implementation task is the Power BI dashboard.

The intended dashboard should provide an executive interface for:

- Enterprise KPI monitoring
- Revenue and gross-profit trends
- Division performance
- Channel performance
- Geographic performance
- Product concentration
- Customer concentration
- Discounting
- Returns
- Target-versus-actual variance
- Management drill-downs

The dashboard should use the validated analytical logic established in PostgreSQL rather than independently recreating business rules without documentation.

### Future maturity path

A more advanced version of the project could also introduce:

1. Driver-based management targets
2. Forecast-versus-actual analysis
3. Scenario planning
4. Contribution-margin analysis
5. Operating-expense allocation
6. EBITDA analysis
7. KPI alerting
8. Predictive forecasting
9. Prescriptive decision support
10. Automated management reporting

These extensions belong to the broader portfolio progression rather than being prerequisites for completion of the current project.

---

## 13. Skills Demonstrated

This project demonstrates a combination of technical, analytical, performance-management, and executive decision-support capabilities.

### Enterprise Performance Management

- KPI definition and measurement
- Actual-versus-target performance analysis
- Variance analysis
- Performance monitoring
- Management reporting
- Identification of performance gaps
- Translation of analytical findings into management priorities
- Understanding of the distinction between actuals, targets, forecasts, and benchmarks
- Consideration of target-setting methodology and governance

### Business Intelligence

- Analytical data modeling
- Dimensional modeling
- Fact and dimension design
- Business-grain definition
- KPI construction
- Data-quality validation
- Reproducible analytical workflows
- Executive reporting design

### SQL and PostgreSQL

- Relational database design
- Table creation
- Primary and foreign keys
- Composite uniqueness constraints
- Check constraints
- Data seeding
- SQL joins
- Common table expressions
- Aggregation
- Conditional aggregation
- Date-based analysis
- Distinct-count analysis
- Variance calculations
- Percentage calculations
- Transaction-level and aggregated analysis
- Query validation
- Join-grain control
- Prevention of aggregation fanout

### Analytical Reasoning

- Enterprise performance analysis
- Trend analysis
- Profitability analysis
- Product concentration analysis
- Customer concentration analysis
- Channel analysis
- Geographic analysis
- Discount analysis
- Returns analysis
- Target-versus-actual analysis
- Cross-dimensional analysis
- Identification of management questions requiring further investigation

### Financial and Commercial Analysis

- Revenue analysis
- Gross-profit analysis
- Gross-margin analysis
- Discount analysis
- Revenue realization
- Return-rate analysis
- Refund analysis
- Estimated gross-profit impact
- Commercial concentration
- Customer and product dependency
- Target and variance interpretation

### Executive Decision Support

- Converting data into management questions
- Building evidence chains
- Separating findings from assumptions
- Translating metrics into implications
- Identifying management priorities
- Distinguishing evidence from recommendations
- Communicating analytical limitations
- Structuring executive reporting

### Data Governance and Analytical Control

- Explicit grain definition
- Referential integrity
- Composite uniqueness
- Validation of target coverage
- Detection and prevention of join multiplication
- Separation of simulated data from external evidence
- Documentation of assumptions
- Reproducible data generation
- Transparent analytical methodology

### Strategic Thinking

The project moves beyond descriptive reporting by asking what management should investigate and act upon.

Examples include:

- Whether growth is sufficiently diversified
- Whether customer concentration creates commercial dependency
- Whether product concentration creates portfolio risk
- Whether channel performance differs materially
- Whether discounting is creating value or eroding realization
- Whether returns create operational or profitability exposure
- Whether target gaps require pricing, volume, mix, or operational intervention
- Whether the existing target methodology is sufficiently decision-useful

### From Data to Business Insight

The purpose of this project is not simply to produce reports or demonstrate technical proficiency. It is to demonstrate how data can be used to understand a business, identify meaningful patterns and risks, generate actionable insights, and support better strategic decisions.

The analytical process connects:

```text
Business Question
        ↓
Data
        ↓
Analysis
        ↓
Business Insight
        ↓
Strategic Implication
        ↓
Management Decision
        ↓
Action
```
This reflects the broader capability the project is designed to demonstrate: connecting business understanding with analytical reasoning and translating evidence into better management decisions.

---

## 14. Portfolio Context

The Enterprise Performance Command Center is **Project 1 of the Aurevia Group portfolio**.

The portfolio is designed as an integrated business transformation and analytics journey rather than eight unrelated technical projects.

Aurevia Group is used as a common fictional company so that analytical decisions made in one project can inform the next.

### Portfolio architecture

The planned portfolio consists of eight linked projects:

1. **Enterprise Performance Command Center**
2. **Market Entry Strategy**
3. **Customer Growth Engine**
4. **Pricing & Revenue Optimization**
5. **Supply Chain Resilience**
6. **Investment & Risk Intelligence**
7. **Predictive Decision Platform**
8. **CEO Strategic Decision Lab**

AI and advanced analytics are treated as cross-cutting capabilities across the portfolio rather than as a standalone ninth project.

### Project 1 — Enterprise Performance Command Center

The first project establishes the enterprise analytical foundation.

Its primary questions are:

- How is Aurevia performing?
- Where is performance strongest and weakest?
- Which divisions, channels, regions, products, and customers drive results?
- Where is concentration creating risk?
- How are discounts affecting revenue realization?
- What operational exposure is visible through returns?
- How does actual performance compare with defined benchmarks?
- Which issues require management investigation?

The project therefore establishes the baseline from which later strategic decisions can be developed.

### Project 2 — Market Entry Strategy

The next stage uses the enterprise performance foundation to evaluate market attractiveness and international expansion.

The analysis can build on:

- Geographic performance
- Regional concentration
- Existing customer exposure
- Channel structure
- Product performance
- Market-level opportunities

The strategic question becomes:

> Where should Aurevia grow next, and why?

### Project 3 — Customer Growth Engine

The customer analytics established in Project 1 provide the foundation for deeper customer strategy.

The focus moves toward:

- Customer acquisition
- Customer segmentation
- Retention
- Customer lifetime value
- Cross-selling
- Customer profitability
- Growth opportunities

The question becomes:

> Which customers should Aurevia acquire, retain, develop, or prioritize?

### Project 4 — Pricing & Revenue Optimization

The discount and revenue-realization analysis from Project 1 creates a foundation for a more sophisticated commercial optimization problem.

The project can examine:

- Pricing
- Discount elasticity
- Product mix
- Channel pricing
- Margin trade-offs
- Revenue realization
- Promotional effectiveness

The question becomes:

> How can Aurevia increase profitable revenue rather than simply increasing volume?

### Project 5 — Supply Chain Resilience

The product, geographic, channel, and returns dimensions can then support operational resilience analysis.

The project can investigate:

- Supply concentration
- Geographic dependencies
- Product availability
- Operational bottlenecks
- Returns
- Disruption scenarios
- Resilience strategies

The question becomes:

> How can Aurevia grow while reducing operational vulnerability?

### Project 6 — Investment & Risk Intelligence

The portfolio then moves from operating performance toward capital allocation and enterprise risk.

The analysis can integrate:

- Market opportunities
- Financial performance
- Geographic exposure
- Customer concentration
- Product concentration
- Supply-chain exposure
- Strategic scenarios

The question becomes:

> Where should Aurevia allocate capital, and what risks should management accept or avoid?

### Project 7 — Predictive Decision Platform

The portfolio then introduces predictive analytics.

Potential capabilities include:

- Revenue forecasting
- Demand forecasting
- Customer churn prediction
- Product demand prediction
- Risk scoring
- Scenario modeling
- Early-warning indicators

The question becomes:

> What is likely to happen next, and how early can management respond?

### Project 8 — CEO Strategic Decision Lab

The final project integrates the portfolio into an executive decision environment.

It can combine:

```text
Historical performance
        +
External market evidence
        +
Forecasts
        +
Scenarios
        +
Risk
        +
Investment options
        +
Strategic priorities
        ↓
CEO decision
```

The final objective is not simply to display more analytics.

It is to demonstrate how an executive can use integrated evidence to evaluate strategic alternatives, understand trade-offs, and make better decisions under uncertainty.

### Portfolio progression

The eight projects are designed to progress from descriptive performance management toward strategic decision intelligence:

```text
1. Measure performance
        ↓
2. Identify where to grow
        ↓
3. Understand customers
        ↓
4. Optimize commercial performance
        ↓
5. Strengthen operational resilience
        ↓
6. Allocate capital and manage risk
        ↓
7. Predict future outcomes
        ↓
8. Make integrated executive decisions
```

This progression is intentional.

Project 1 establishes the analytical foundation required for the subsequent projects.

### Why Project 1 matters within the portfolio

A strategic portfolio cannot begin with prediction or advanced AI without first establishing reliable performance measurement.

Project 1 therefore provides the foundation for:

- KPI governance
- Enterprise performance visibility
- Analytical discipline
- Data-modeling standards
- Evidence traceability
- Management reporting
- Target and variance concepts
- Decision-oriented analytics

The later projects can reuse these principles while increasing analytical sophistication.

### Portfolio design principle

The portfolio is built around the progression:

```text
Data
→ Information
→ Insight
→ Decision
→ Action
→ Learning
```

The Enterprise Performance Command Center occupies the first major decision-support stage of that journey.

It demonstrates that analytics is valuable not because it produces more numbers, but because it helps management understand **what is happening, why it matters, what should be investigated, and where action may create value**.

### Final portfolio principle

The ultimate objective of the Aurevia portfolio is to show a progression from:

> **"Can I analyze data?"**

to:

> **"Can I use evidence, analytics, strategy, and structured reasoning to help a business make better decisions?"**

Project 1 establishes that foundation.
