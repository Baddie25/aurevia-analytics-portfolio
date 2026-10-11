# Aurevia Group — Project 1 Data Dictionary

## 1. Purpose

This data dictionary documents the analytical data model used in **Project 1 — Enterprise Performance Command Center**.

It defines:

- The purpose and grain of each table
- The meaning of individual fields
- Primary and foreign-key relationships
- Core business measures used in the analysis
- How returns and performance targets should be interpreted
- Analytical and aggregation considerations relevant to SQL analysis and reporting

The dictionary is intended to provide a common reference for the SQL analysis, validation work, executive reporting, and future Power BI dashboard.

The model consists of **nine dimension tables and three fact tables**:

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

The seed data establishes four business divisions, three regions, thirteen countries, five sales channels, twelve products, twelve salespeople, and twenty-four customers. :contentReference[oaicite:0]{index=0}

---

## 2. Data Model Overview

The database follows a dimensional analytical structure in which descriptive dimensions provide the context for transactional and planning facts.

### 2.1 Dimensions

Dimension tables describe the entities used to analyse performance:

```text
Date
 ├── Division
 ├── Region
 │    └── Cluster
 │         └── Country
 ├── Channel
 ├── Customer
 ├── Product
 └── Salesperson
```

The geographic hierarchy is:

```text
Global
   ↓
Region
   ↓
Cluster
   ↓
Country
```

`dim_cluster` was introduced through a database migration and provides an intermediate geographic grouping between region and country.

### 2.2 Fact tables

The model contains three distinct fact tables:

```text
fact_sales
    ↓
Sales transactions

fact_returns
    ↓
Returned sales lines associated with original sales

fact_targets
    ↓
Illustrative performance benchmarks
```

Keeping `fact_returns` separate from `fact_sales` allows returned quantities and refunds to be analysed without embedding return transactions into the original sales fact.

---

# 3. Table Inventory

| Table | Type | Primary analytical purpose | Grain |
|---|---|---|---|
| `dim_date` | Dimension | Calendar and time analysis | One row per calendar date |
| `dim_division` | Dimension | Business division analysis | One row per division |
| `dim_region` | Dimension | Regional analysis | One row per region |
| `dim_cluster` | Dimension | Geographic cluster analysis | One row per region-cluster combination |
| `dim_country` | Dimension | Country analysis | One row per country |
| `dim_channel` | Dimension | Sales-channel analysis | One row per channel |
| `dim_customer` | Dimension | Customer and customer-segment analysis | One row per customer |
| `dim_product` | Dimension | Product and category analysis | One row per product |
| `dim_salesperson` | Dimension | Salesperson analysis | One row per salesperson |
| `fact_sales` | Fact | Transactional sales and profitability analysis | One product line within a customer order |
| `fact_returns` | Fact | Returns and refund analysis | One returned product line associated with a sales line |
| `fact_targets` | Fact | Target-versus-actual analysis | One date × division × region × channel target record |

---

# 4. Dimension Tables

## 4.1 `dim_date`

### Purpose

Provides the calendar structure used for time-based analysis, including annual, quarterly, monthly, and weekly reporting.

The date dimension is populated daily from **2022-01-01 through 2026-12-31**. :contentReference[oaicite:1]{index=1}

### Grain

One row per calendar date.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `date_key` | INTEGER | Surrogate key identifying the calendar date | Primary key and date-dimension join key |
| `full_date` | DATE | Actual calendar date | Used to join transactional dates and target dates |
| `year` | INTEGER | Calendar year | Annual reporting |
| `quarter` | INTEGER | Calendar quarter | Quarterly reporting |
| `month` | INTEGER | Calendar month number | Monthly reporting and sorting |
| `month_name` | VARCHAR | Calendar month name | Human-readable reporting |
| `week_of_year` | INTEGER | Week number within the year | Weekly analysis |

### Analytical notes

`full_date` is the business date used by transactional facts. The `date_key` provides the dimensional key used by the model.

The date dimension extends into 2026 to provide future calendar capacity even though the seeded transaction and target data do not extend through the entire calendar range.

---

## 4.2 `dim_division`

### Purpose

Defines Aurevia Group's major business divisions.

The seeded divisions are:

- Personal Care
- Home & Lifestyle
- Wellness
- Everyday Essentials :contentReference[oaicite:2]{index=2}

### Grain

One row per business division.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `division_id` | SERIAL / INTEGER | Unique identifier for the division | Primary key |
| `division_name` | VARCHAR | Business division name | Division-level reporting and grouping |

---

## 4.3 `dim_region`

### Purpose

Defines Aurevia Group's major geographic regions.

The seeded regions are:

- Europe
- North America
- Emerging Markets :contentReference[oaicite:3]{index=3}

### Grain

One row per region.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `region_id` | SERIAL / INTEGER | Unique identifier for the region | Primary key |
| `region_name` | VARCHAR | Geographic region name | Regional reporting and grouping |

---

## 4.4 `dim_cluster`

### Purpose

Provides an intermediate geographic management hierarchy between region and country.

Clusters were introduced through the geographic migration to support more granular regional analysis without treating every country as an independent management region.

### Grain

One row per region-cluster combination.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `cluster_id` | SERIAL / INTEGER | Unique identifier for the geographic cluster | Primary key |
| `region_id` | INTEGER | Region to which the cluster belongs | Foreign key to `dim_region` |
| `cluster_name` | VARCHAR | Management-defined geographic cluster name | Cluster-level reporting |

### Analytical notes

The geographic hierarchy is:

```text
Region
   ↓
Cluster
   ↓
Country
```

The combination of `region_id` and `cluster_name` is unique.

---

## 4.5 `dim_country`

### Purpose

Defines the countries in which Aurevia operates or has customers.

The seeded model contains thirteen countries across Europe, North America, and Emerging Markets. :contentReference[oaicite:4]{index=4}

### Grain

One row per country.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `country_id` | SERIAL / INTEGER | Unique identifier for the country | Primary key |
| `country_name` | VARCHAR | Country name | Country-level reporting |
| `country_code` | CHAR(2) | Two-character country code | Country identification |
| `region_id` | INTEGER | Region containing the country | Foreign key to `dim_region` |
| `cluster_id` | INTEGER | Geographic cluster containing the country | Foreign key to `dim_cluster` |

### Analytical notes

`region_id` and `cluster_id` provide two levels of geographic aggregation.

Country therefore supports:

```text
Global → Region → Cluster → Country
```

---

## 4.6 `dim_channel`

### Purpose

Defines the commercial channels through which Aurevia sells.

The seeded channels are:

- Retail
- E-commerce
- Distributors
- Direct-to-Consumer
- Specialty :contentReference[oaicite:5]{index=5}

### Grain

One row per sales channel.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `channel_id` | SERIAL / INTEGER | Unique identifier for the sales channel | Primary key |
| `channel_name` | VARCHAR | Sales-channel name | Channel-level reporting |

---

## 4.7 `dim_customer`

### Purpose

Defines customers and their commercial characteristics.

The seeded customer population contains 24 customers with customer type, geography, channel, segment, acquisition date, and active-status attributes. :contentReference[oaicite:6]{index=6}

### Grain

One row per customer.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `customer_id` | SERIAL / INTEGER | Unique identifier for the customer | Primary key |
| `customer_code` | VARCHAR | Business/customer reference code | Business identifier |
| `customer_name` | VARCHAR | Customer or account name | Customer reporting |
| `customer_type` | VARCHAR | Broad customer classification | Customer-type analysis |
| `country_id` | INTEGER | Country associated with the customer | Foreign key to `dim_country` |
| `channel_id` | INTEGER | Primary sales channel associated with the customer | Foreign key to `dim_channel` |
| `customer_segment` | VARCHAR | Customer segmentation classification | Segment analysis |
| `acquisition_date` | DATE | Date on which the customer was acquired | Customer lifecycle analysis |
| `is_active` | BOOLEAN | Indicates whether the customer is currently active | Active-customer filtering |

### Analytical notes

Customer concentration analysis should use `net_sales_amount` from `fact_sales` rather than customer counts alone.

---

## 4.8 `dim_product`

### Purpose

Defines the products sold by Aurevia and their commercial and cost characteristics.

The seeded catalogue contains twelve products across the four divisions, with standard cost, list price, launch date, and active status. :contentReference[oaicite:7]{index=7}

### Grain

One row per product.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `product_id` | SERIAL / INTEGER | Unique identifier for the product | Primary key |
| `product_code` | VARCHAR | Business product code | Business identifier |
| `product_name` | VARCHAR | Product name | Product reporting |
| `category_name` | VARCHAR | Product category | Category-level analysis |
| `division_id` | INTEGER | Division responsible for the product | Foreign key to `dim_division` |
| `standard_cost` | NUMERIC | Standard unit product cost | Cost and profitability analysis |
| `list_price` | NUMERIC | Standard listed unit selling price | Pricing and discount analysis |
| `launch_date` | DATE | Product launch date | Product lifecycle analysis |
| `is_active` | BOOLEAN | Indicates whether the product is currently active | Active-product filtering |

### Analytical notes

`standard_cost` represents the seeded standard product cost used to calculate product cost in the sales fact.

`list_price` represents the product's reference selling price before the transaction-level pricing and discount treatment in `fact_sales`.

---

## 4.9 `dim_salesperson`

### Purpose

Defines the salespeople associated with sales transactions.

The seeded model contains twelve salespeople with region, channel, hire-date, and active-status attributes. :contentReference[oaicite:8]{index=8}

### Grain

One row per salesperson.

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `salesperson_id` | SERIAL / INTEGER | Unique identifier for the salesperson | Primary key |
| `salesperson_code` | VARCHAR | Business salesperson reference code | Business identifier |
| `salesperson_name` | VARCHAR | Salesperson name | Salesperson reporting |
| `region_id` | INTEGER | Region associated with the salesperson | Foreign key to `dim_region` |
| `channel_id` | INTEGER | Channel associated with the salesperson | Foreign key to `dim_channel` |
| `hire_date` | DATE | Salesperson hire date | Workforce tenure analysis |
| `is_active` | BOOLEAN | Indicates whether the salesperson is currently active | Active-salesperson filtering |

---

# 5. Fact Tables

## 5.1 `fact_sales`

### Purpose

Stores the core transactional sales data used for revenue, discount, volume, cost, and profitability analysis.

### Grain

**One product line within a customer order.**

An order may therefore contain multiple rows in `fact_sales`.

The seeded sales data contains 1,500 generated orders with one to three product lines per order. Transaction-level quantities, pricing, discounts, product costs, and gross profit are calculated at the sales-line level. :contentReference[oaicite:9]{index=9}

### Columns

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `sales_id` | BIGSERIAL / BIGINT | Unique identifier for the sales line | Primary key |
| `order_id` | VARCHAR | Customer order identifier | Order-level grouping |
| `order_line_number` | INTEGER | Line number within the order | Sales-line identification |
| `order_date` | DATE | Date on which the order was placed | Date analysis |
| `customer_id` | INTEGER | Customer associated with the order | Foreign key to `dim_customer` |
| `product_id` | INTEGER | Product sold | Foreign key to `dim_product` |
| `salesperson_id` | INTEGER | Salesperson associated with the sale | Foreign key to `dim_salesperson`; nullable |
| `quantity` | INTEGER | Number of units sold on the sales line | Volume analysis |
| `unit_list_price` | NUMERIC | Unit list/reference selling price recorded on the transaction | Pricing analysis |
| `discount_amount` | NUMERIC | Total monetary discount applied to the sales line | Discount analysis |
| `unit_cost` | NUMERIC | Unit product cost associated with the sales line | Cost analysis |
| `gross_sales_amount` | NUMERIC | Sales value before transaction discount | Gross revenue analysis |
| `net_sales_amount` | NUMERIC | Sales value after transaction discount | Primary revenue measure |
| `product_cost_amount` | NUMERIC | Total product cost associated with the sales line | Cost-of-goods analysis |
| `gross_profit_amount` | NUMERIC | Net sales less product cost | Gross-profit analysis |
| `created_at` | TIMESTAMP | Timestamp at which the record was created | Technical/audit field |

### Core relationships

```text
fact_sales.order_date
    → dim_date.full_date

fact_sales.customer_id
    → dim_customer.customer_id

fact_sales.product_id
    → dim_product.product_id

fact_sales.salesperson_id
    → dim_salesperson.salesperson_id
```

### Business logic

At the sales-line level:

```text
Gross Sales
    = Quantity × Unit List Price

Net Sales
    = Gross Sales − Discount Amount

Product Cost
    = Quantity × Unit Cost

Gross Profit
    = Net Sales − Product Cost
```

The seeded sales data applies deterministic pricing and discount logic to generate the simulated transaction data. :contentReference[oaicite:10]{index=10}

---

## 5.2 `fact_returns`

### Purpose

Stores product returns separately from the original sales transactions.

This table is used to analyse:

- Returned units
- Return rates
- Refund values
- Return reasons
- Return timing
- Estimated gross-profit impact of returns

### Grain

**One returned product line associated with an original sales line.**

Each return references the original transaction through `sales_id`.

### Columns

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `return_id` | BIGSERIAL / BIGINT | Unique identifier for the return record | Primary key |
| `order_id` | VARCHAR | Original customer order identifier | Order-level return analysis |
| `sales_id` | BIGINT | Original sales-line identifier associated with the return | Foreign key to `fact_sales` |
| `return_date` | DATE | Date on which the return was recorded | Return timing analysis |
| `customer_id` | INTEGER | Customer associated with the return | Customer return analysis |
| `product_id` | INTEGER | Product returned | Product return analysis |
| `returned_quantity` | INTEGER | Number of units returned | Return-volume analysis |
| `return_reason` | VARCHAR | Reason recorded for the return | Root-cause analysis |
| `refund_amount` | NUMERIC | Monetary refund associated with the returned line | Refund-value analysis |
| `created_at` | TIMESTAMP | Timestamp at which the return record was created | Technical/audit field |

### Core relationships

```text
fact_returns.sales_id
    → fact_sales.sales_id

fact_returns.customer_id
    → dim_customer.customer_id

fact_returns.product_id
    → dim_product.product_id

fact_returns.return_date
    → dim_date.full_date
```

### Analytical notes

Returns should be aggregated independently before being joined to sales-level or monthly sales analysis.

This avoids **join multiplication**, where multiple return rows joined directly to multiple sales rows could artificially inflate revenue, profit, or return measures.

The seeded return data selects eligible sales lines, creates a returned quantity, assigns a return reason, and calculates a refund amount based on the associated sales transaction. :contentReference[oaicite:11]{index=11}

---

## 5.3 `fact_targets`

### Purpose

Stores illustrative performance benchmarks used to demonstrate target-versus-actual analysis.

### Grain

**One target record per date × division × region × channel combination.**

The target data is generated after the sales data is available. Revenue, gross-profit, and order targets are based on the simulated baseline actuals with a 5% uplift. :contentReference[oaicite:12]{index=12}

### Columns

| Column | Type | Definition | Analytical role |
|---|---|---|---|
| `target_id` | BIGSERIAL / BIGINT | Unique identifier for the target record | Primary key |
| `target_date` | DATE | Date associated with the target record | Time analysis |
| `division_id` | INTEGER | Division to which the target applies | Foreign key to `dim_division` |
| `region_id` | INTEGER | Region to which the target applies | Foreign key to `dim_region` |
| `channel_id` | INTEGER | Channel to which the target applies | Foreign key to `dim_channel` |
| `revenue_target` | NUMERIC | Illustrative revenue benchmark | Revenue variance analysis |
| `gross_profit_target` | NUMERIC | Illustrative gross-profit benchmark | Profit variance analysis |
| `order_target` | NUMERIC / INTEGER | Illustrative order-volume benchmark | Order variance analysis |
| `created_at` | TIMESTAMP | Timestamp at which the target record was created | Technical/audit field |

### Target interpretation

These targets are **synthetic retrospective planning benchmarks**, not historical management budgets, approved targets, or forecasts.

The methodology applies a 5% uplift to the simulated baseline actuals:

```text
Revenue Target
    = Baseline Revenue × 1.05

Gross Profit Target
    = Baseline Gross Profit × 1.05

Order Target
    = Baseline Distinct Orders × 1.05
```

This construction is intentionally transparent and is used to demonstrate target-versus-actual analytical capability in a fictional-company portfolio context.

It should not be interpreted as evidence of Aurevia management's actual planning process.

---

# 6. Key Relationships

The principal relationships in the analytical model are:

```text
                         dim_date
                            │
              ┌─────────────┼──────────────┐
              │             │              │
              ▼             ▼              ▼
         fact_sales   fact_returns   fact_targets
              │
      ┌───────┼────────┬────────────┐
      ▼       ▼        ▼            ▼
 customer  product  salesperson   date
      │       │
      ▼       ▼
 country   division
      │
      ▼
   cluster
      │
      ▼
    region
```

More specifically:

### Sales relationships

```text
fact_sales.order_date
    → dim_date.full_date

fact_sales.customer_id
    → dim_customer.customer_id

fact_sales.product_id
    → dim_product.product_id

fact_sales.salesperson_id
    → dim_salesperson.salesperson_id
```

### Customer geography

```text
dim_customer.country_id
    → dim_country.country_id

dim_country.cluster_id
    → dim_cluster.cluster_id

dim_country.region_id
    → dim_region.region_id

dim_cluster.region_id
    → dim_region.region_id
```

### Product hierarchy

```text
dim_product.division_id
    → dim_division.division_id
```

### Return relationships

```text
fact_returns.sales_id
    → fact_sales.sales_id

fact_returns.return_date
    → dim_date.full_date
```

### Target relationships

```text
fact_targets.target_date
    → dim_date.full_date

fact_targets.division_id
    → dim_division.division_id

fact_targets.region_id
    → dim_region.region_id

fact_targets.channel_id
    → dim_channel.channel_id
```

---

# 7. Business Measures

## 7.1 Gross Revenue

Gross revenue represents the sales value before transaction-level discounts.

```text
Gross Revenue
    = SUM(gross_sales_amount)
```

---

## 7.2 Discounts

Discount value represents the monetary reduction applied to gross sales.

```text
Discount Value
    = SUM(discount_amount)
```

---

## 7.3 Net Revenue

Net revenue is the primary sales-value measure used throughout the project.

```text
Net Revenue
    = SUM(net_sales_amount)
```

At the transaction level:

```text
Net Sales
    = Gross Sales − Discount Amount
```

---

## 7.4 Product Cost

Product cost represents the cost of the units sold.

```text
Product Cost
    = SUM(product_cost_amount)
```

---

## 7.5 Gross Profit

Gross profit represents revenue remaining after product cost.

```text
Gross Profit
    = SUM(gross_profit_amount)
```

At the sales-line level:

```text
Gross Profit
    = Net Sales − Product Cost
```

---

## 7.6 Gross Margin

Gross margin expresses gross profit as a percentage of net revenue.

```text
Gross Margin
    = Gross Profit ÷ Net Revenue
```

When expressed as a percentage:

```text
Gross Margin %
    = (Gross Profit ÷ Net Revenue) × 100
```

Gross margin should be calculated from aggregated revenue and gross profit rather than averaging row-level margin percentages.

---

## 7.7 Enterprise Discount Rate

The enterprise discount rate measures discounts as a proportion of gross sales.

```text
Discount Rate
    = Discount Value ÷ Gross Revenue
```

This should be calculated from aggregated values at the required reporting level.

---

## 7.8 Units Sold

```text
Units Sold
    = SUM(fact_sales.quantity)
```

This measure represents the quantity recorded as sold on the sales transactions.

---

## 7.9 Returned Units

```text
Returned Units
    = SUM(fact_returns.returned_quantity)
```

Returned units should be sourced from `fact_returns`, not inferred from `fact_sales`.

---

## 7.10 Return Rate

The project uses returned units relative to units sold:

```text
Return Rate
    = Returned Units ÷ Units Sold
```

When expressed as a percentage:

```text
Return Rate %
    = (Returned Units ÷ Units Sold) × 100
```

The return rate should be calculated using compatible reporting periods and dimensions.

---

## 7.11 Refund Value

Refund value represents the monetary value recorded in the returns fact.

```text
Refund Value
    = SUM(fact_returns.refund_amount)
```

Refund value is distinct from the estimated gross-profit impact of returns.

---

## 7.12 Estimated Gross-Profit Impact of Returns

The project estimates the gross-profit impact of returned units using the refund value and associated product cost.

Conceptually:

```text
Estimated GP Impact
    = Refund Value − Estimated Product Cost of Returned Units
```

This is an **analytical estimate**, not a complete accounting treatment of returns.

It should therefore be labelled as an estimated gross-profit impact in executive reporting.

---

# 8. Target and Variance Measures

## 8.1 Revenue Variance

```text
Revenue Variance
    = Actual Revenue − Revenue Target
```

A positive value indicates actual revenue exceeded the benchmark.

A negative value indicates actual revenue fell below the benchmark.

---

## 8.2 Revenue Variance %

```text
Revenue Variance %
    = (Actual Revenue − Revenue Target)
      ÷ Revenue Target
```

---

## 8.3 Gross-Profit Variance

```text
Gross-Profit Variance
    = Actual Gross Profit − Gross-Profit Target
```

---

## 8.4 Gross-Profit Variance %

```text
Gross-Profit Variance %
    = (Actual Gross Profit − Gross-Profit Target)
      ÷ Gross-Profit Target
```

---

## 8.5 Order Variance

```text
Order Variance
    = Actual Orders − Order Target
```

---

## 8.6 Target Margin

A target gross margin can be derived from the target revenue and gross-profit fields:

```text
Target Gross Margin
    = Gross-Profit Target ÷ Revenue Target
```

This derived measure is not stored directly in `fact_targets`.

---

# 9. Target Data Interpretation

The target framework in this project should be interpreted carefully.

The target records were created specifically to demonstrate performance-management and variance-analysis techniques in the absence of genuine historical management budgets for the fictional company.

The methodology uses simulated baseline actuals and applies a 5% uplift to establish illustrative benchmarks. :contentReference[oaicite:13]{index=13}

Therefore:

| Term | Interpretation in Project 1 |
|---|---|
| Actual | Simulated transactional performance from `fact_sales` |
| Target | Synthetic planning benchmark from `fact_targets` |
| Budget | Not represented |
| Forecast | Not represented |
| Historical management target | Not represented |
| Benchmark | Illustrative retrospective benchmark |

The targets should therefore be described as **illustrative planning benchmarks** rather than genuine historical targets.

A future production-style model could replace these with driver-based management targets, approved budgets, forecasts, or independently constructed benchmarks.

---

# 10. Data Quality and Constraints

The database applies structural constraints to improve data integrity.

Important examples include:

### Primary keys

Each dimension and fact table has a unique primary key.

### Foreign keys

Fact and dimension relationships are enforced through foreign-key constraints.

### Uniqueness

Examples include:

- Unique customer codes
- Unique product codes
- Unique salesperson codes
- Unique country codes
- Unique sales order and line-number combinations
- Unique target combinations by target date, division, region, and channel

### Positive transaction quantities

Sales quantities and returned quantities must be greater than zero.

### Non-negative monetary fields

Sales prices, discounts, costs, targets, and refund amounts are constrained to non-negative values.

### Sales consistency

The sales model enforces relationships such as:

```text
Discount Amount ≤ Gross Sales Amount

Net Sales Amount ≤ Gross Sales Amount
```

### Geographic completeness

Countries must be assigned to a geographic cluster following the geographic migration.

---

# 11. Analytical Grain and Aggregation Guidance

Correct grain awareness is essential when querying this model.

## 11.1 `fact_sales`

The grain is:

```text
One product line within one customer order
```

Therefore:

```sql
COUNT(*)
```

counts sales lines, not orders.

To count orders:

```sql
COUNT(DISTINCT order_id)
```

should be used.

---

## 11.2 `fact_returns`

The grain is:

```text
One returned product line associated with a sales line
```

Returns should normally be aggregated separately before joining to sales performance.

This prevents multiple fact rows from multiplying each other's measures.

---

## 11.3 `fact_targets`

The target grain is:

```text
Date × Division × Region × Channel
```

Actual sales should therefore be aggregated to the same grain before joining to `fact_targets`.

This is particularly important because joining target records directly to lower-grain sales transactions would duplicate target values.

---

## 11.4 Order-count caution

An individual order can contain multiple products and therefore multiple divisions.

Consequently, when actual sales are grouped simultaneously by division, region, and channel, a distinct order count is unique **within that analytical segment**, but the resulting segment-level order counts should not automatically be summed to represent enterprise-wide unique orders.

For enterprise-wide order counts, calculate:

```sql
COUNT(DISTINCT order_id)
```

at the enterprise reporting grain.

---

## 11.5 Revenue and profitability measures

Revenue and gross-profit measures should generally be aggregated from their underlying monetary columns:

```sql
SUM(net_sales_amount)
SUM(gross_profit_amount)
```

Derived ratios such as gross margin and discount rate should then be calculated from the aggregated totals.

Avoid averaging row-level percentages when producing enterprise or management-level metrics.

---

# 12. Seeded Data Coverage

The project uses simulated data designed to support multi-year enterprise performance analysis.

### Dimensions

The seed data establishes:

- 4 business divisions
- 3 geographic regions
- 13 countries
- 5 sales channels
- 12 products
- 12 salespeople
- 24 customers :contentReference[oaicite:14]{index=14} :contentReference[oaicite:15]{index=15} :contentReference[oaicite:16]{index=16} :contentReference[oaicite:17]{index=17}

### Date dimension

The calendar dimension covers:

```text
2022-01-01 → 2026-12-31
```

:contentReference[oaicite:18]{index=18}

### Sales

The seeded sales model generates 1,500 orders with one to three product lines per order. :contentReference[oaicite:19]{index=19}

### Returns

Returns are generated as separate records associated with original sales lines. :contentReference[oaicite:20]{index=20}

### Targets

Targets are generated after the sales data and use a synthetic 5% uplift over the simulated baseline. :contentReference[oaicite:21]{index=21}

---

# 13. Data Dictionary Summary

The model can be understood through three analytical layers:

```text
DESCRIPTIVE CONTEXT
────────────────────────────────────

Date
Division
Region
Cluster
Country
Channel
Customer
Product
Salesperson


TRANSACTIONAL PERFORMANCE
────────────────────────────────────

fact_sales
    ↓
Revenue
Discounts
Units
Product Cost
Gross Profit
Gross Margin


CUSTOMER EXPERIENCE / RETURNS
────────────────────────────────────

fact_returns
    ↓
Returned Units
Return Rate
Refund Value
Return Reasons
Estimated GP Impact


PERFORMANCE MANAGEMENT
────────────────────────────────────

fact_targets
    ↓
Revenue Target
Gross-Profit Target
Order Target
        ↓
Variance Analysis
        ↓
Management Action
```

The central analytical principle is that **dimensions provide business context, facts provide measurable events or benchmarks, and the correct analytical grain determines how those measures can be safely aggregated and compared.**

---

# 14. Analytical Coverage

The data model is designed to support performance analysis across multiple management dimensions, including:

1. Enterprise-level performance
2. Year-over-year performance
3. Division
4. Region
5. Geographic cluster
6. Country
7. Channel
8. Product
9. Product category
10. Customer
11. Customer segment
12. Salesperson

Core performance measures should be evaluated consistently across these dimensions where the underlying data supports the analysis.

KPI definitions should remain consistent across SQL analysis, Python-based validation or analysis, and future Power BI reporting.


