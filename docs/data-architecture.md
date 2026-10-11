# Aurevia Group — Data Architecture

## 1. Purpose

This document defines the data architecture for Aurevia Group's analytics portfolio.

The architecture establishes how business data is organized, related, validated, and progressively extended across the eight-project portfolio.

It serves two purposes:

1. Define the **implemented analytical architecture** supporting Project 1 — Enterprise Performance Command Center.
2. Provide a **long-term architectural blueprint** for extending the data universe across customer, pricing, operations, finance, market, risk, predictive analytics, and executive decision-support projects.

The architecture is designed to support:

- Business performance analysis
- Strategic decision-making
- Financial modelling
- Customer analytics
- Pricing and revenue optimization
- Supply chain management
- Investment and risk analysis
- Predictive analytics
- Executive reporting and decision support

Project-specific implementation should remain incremental. Future-domain tables described in this document represent the planned architecture and should only be implemented when required by a project's analytical objectives.

---

# 2. Data Architecture Principles

The Aurevia analytics architecture follows these principles:

### 2.1 Consistent business vocabulary

Business entities, measures, dimensions, and analytical concepts should use consistent terminology across SQL, Python, Power BI, documentation, and executive reporting.

### 2.2 Explicit fact-table grain

Every fact table must have a clearly defined analytical grain.

This prevents incorrect aggregation, duplicate counting, and join multiplication.

### 2.3 Relational integrity

Primary keys and foreign keys should establish explicit relationships between dimensions and facts.

### 2.4 Separation of business events and analytical benchmarks

Transactional events, such as sales and returns, should remain separate from planning benchmarks and analytical outputs.

For Project 1:

```text
fact_sales
    ↓
Transactional sales

fact_returns
    ↓
Return transactions

fact_targets
    ↓
Illustrative performance benchmarks
```

### 2.5 Separation of source data and analytical outputs

Transactional and descriptive data should remain distinct from derived analytical outputs such as forecasts, predictions, scores, recommendations, and optimization results.

### 2.6 Document assumptions and lineage

Important assumptions, calculation rules, target methodologies, and relationships should be documented so analytical results can be traced back to their underlying data.

### 2.7 Validate before decision-making

Data should be validated before being used for business analysis or management decisions.

Validation should include structural integrity, completeness, reconciliation, grain checks, and business-rule checks.

### 2.8 Incremental architecture development

The data universe should be developed progressively.

Only the tables required to answer the defined analytical questions of each project should be implemented at that stage.

---

# 3. Architecture Layers

The portfolio architecture can be viewed through four broad layers:

```text
                    BUSINESS DATA
                         │
                         ▼
              ┌─────────────────────┐
              │ Dimensions & Facts  │
              │ PostgreSQL          │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Analytical SQL      │
              │ Validation / Python │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Analytical Outputs  │
              │ Power BI / Reports  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Executive Decision  │
              │ Support             │
              └─────────────────────┘
```

The architecture therefore separates:

- Data storage
- Analytical processing
- Reporting
- Decision support

---

# 4. Major Data Domains

The long-term Aurevia data architecture consists of the following domains:

| Domain | Purpose |
|---|---|
| Commercial | Sales, customers, products, orders, channels, and commercial performance |
| Marketing & Customer | Customer segmentation, acquisition, retention, campaigns, activity, and experimentation |
| Pricing | Product prices, discounts, promotions, competitor prices, and pricing analysis |
| Operations | Suppliers, inventory, warehouses, shipments, logistics, and lead times |
| Finance | Costs, budgets, expenses, investments, and cash flows |
| Market & Macro | Market size, market growth, competitors, macroeconomic indicators, and FX |
| Risk & Scenarios | Risk factors, risk events, scenarios, assumptions, outcomes, and simulations |
| Analytics | Forecasts, predictions, scores, recommendations, and optimization outputs |

These domains form the long-term portfolio architecture. Their implementation will occur progressively across the eight projects.

---

# 5. Project 1 Implemented Architecture

Project 1 establishes the commercial and performance foundation of the Aurevia analytical model.

The implemented Project 1 model contains:

### Dimension tables

```text
dim_date
dim_division
dim_region
dim_cluster
dim_country
dim_channel
dim_customer
dim_product
dim_salesperson
```

### Fact tables

```text
fact_sales
fact_returns
fact_targets
```

The model therefore contains **nine dimension tables and three fact tables**.

---

# 6. Project 1 Dimensional Architecture

## 6.1 `dim_date`

Provides the calendar structure used for time-based analysis.

The date dimension supports:

- Year
- Quarter
- Month
- Month name
- Week
- Full calendar date

The calendar is populated from 2022 through 2026 to provide sufficient date capacity for the portfolio.

---

## 6.2 `dim_division`

Defines Aurevia's business divisions.

The current model contains:

- Personal Care
- Home & Lifestyle
- Wellness
- Everyday Essentials

Products are associated with divisions through `dim_product`.

---

## 6.3 `dim_region`

Defines Aurevia's major geographic regions:

- Europe
- North America
- Emerging Markets

Regions form the highest geographic management level below the enterprise.

---

## 6.4 `dim_cluster`

Provides a management-defined geographic grouping between region and country.

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

Clusters allow management to analyse groups of countries without treating every country as an independent management region.

---

## 6.5 `dim_country`

Defines individual Aurevia markets.

Each country belongs to:

- A region
- A geographic cluster

The resulting hierarchy is:

```text
dim_region
     │
     ▼
dim_cluster
     │
     ▼
dim_country
```

---

## 6.6 `dim_channel`

Defines Aurevia's commercial channels.

The current model contains:

- Retail
- E-commerce
- Distributors
- Direct-to-Consumer
- Specialty

Channel is associated with customers through `dim_customer.channel_id`.

---

## 6.7 `dim_customer`

Defines customers and their commercial attributes.

Customers are associated with:

- Country
- Channel
- Customer type
- Customer segment
- Acquisition date
- Active status

The customer dimension provides the main path from sales transactions to customer and geographic analysis.

---

## 6.8 `dim_product`

Defines the products sold by Aurevia.

Products are associated with:

- Product category
- Division
- Standard cost
- List price
- Launch date
- Active status

The product-to-division relationship is:

```text
dim_division
     │
     ▼
dim_product
```

---

## 6.9 `dim_salesperson`

Defines the salespeople associated with sales transactions.

Salespeople may be associated with:

- Region
- Channel
- Hire date
- Active status

The relationship to sales is optional because `fact_sales.salesperson_id` is nullable.

---

# 7. Project 1 Fact Architecture

## 7.1 `fact_sales`

### Purpose

Stores Aurevia's transactional sales activity.

### Grain

**One product line within one customer order.**

For example:

```text
Order ORD-000001

Product A → one fact_sales row
Product B → one fact_sales row
Product C → one fact_sales row
```

An order containing three products therefore produces three sales-line records.

### Core analytical measures

`fact_sales` contains measures including:

- Quantity
- Unit list price
- Discount amount
- Unit cost
- Gross sales amount
- Net sales amount
- Product cost amount
- Gross profit amount

### Primary relationships

```text
fact_sales.customer_id
        ↓
dim_customer.customer_id

fact_sales.product_id
        ↓
dim_product.product_id

fact_sales.salesperson_id
        ↓
dim_salesperson.salesperson_id

fact_sales.order_date
        ↓
dim_date.full_date
```

### Analytical implications

Because the fact table is at sales-line grain:

```text
COUNT(*)
```

counts sales lines, not customer orders.

Enterprise order counts should therefore use:

```text
COUNT(DISTINCT order_id)
```

when an order-level measure is required.

---

## 7.2 `fact_returns`

### Purpose

Stores returned product lines separately from the original sales transactions.

This supports analysis of:

- Returned units
- Return rates
- Refund value
- Return reasons
- Return timing
- Estimated gross-profit impact

### Grain

**One returned product line associated with an original sales line.**

The return is linked to the original transaction through `sales_id`.

### Primary relationship

```text
fact_returns.sales_id
        ↓
fact_sales.sales_id
```

Additional dimensional relationships include:

```text
fact_returns.customer_id
        ↓
dim_customer.customer_id

fact_returns.product_id
        ↓
dim_product.product_id

fact_returns.return_date
        ↓
dim_date.full_date
```

### Analytical implications

Returns should normally be aggregated separately before being joined to sales performance.

This prevents multiple sales and return records from multiplying each other's measures during joins.

---

## 7.3 `fact_targets`

### Purpose

Stores illustrative performance benchmarks for target-versus-actual analysis.

### Grain

**One target record per date × division × region × channel combination.**

The targets represent monthly planning periods in the current Project 1 implementation.

### Relationships

```text
fact_targets.target_date
        ↓
dim_date.full_date

fact_targets.division_id
        ↓
dim_division.division_id

fact_targets.region_id
        ↓
dim_region.region_id

fact_targets.channel_id
        ↓
dim_channel.channel_id
```

### Interpretation

The target data is synthetic and retrospective.

It applies a 5% uplift to simulated baseline actuals to create illustrative planning benchmarks.

Therefore:

```text
fact_targets ≠ historical management budget
fact_targets ≠ approved management target
fact_targets ≠ independent forecast
```

The target framework exists to demonstrate target-versus-actual and variance-analysis capability.

---

# 8. Project 1 Relationship Architecture

The primary Project 1 relationships can be represented as follows:

```text
                              dim_date
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
            fact_sales      fact_returns      fact_targets
                 │
       ┌─────────┼──────────┐
       │         │          │
       ▼         ▼          ▼
dim_customer  dim_product  dim_salesperson
       │         │
       │         ▼
       │    dim_division
       │
       ▼
 dim_country
       │
       ▼
 dim_cluster
       │
       ▼
 dim_region
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

The customer-to-geography path is:

```text
fact_sales
    ↓
dim_customer
    ↓
dim_country
    ↓
dim_cluster
    ↓
dim_region
```

The product-to-division path is:

```text
fact_sales
    ↓
dim_product
    ↓
dim_division
```

---

# 9. Channel Architecture

The current Project 1 model assigns channel at the customer level.

The relationship is:

```text
fact_sales
    ↓
customer_id
    ↓
dim_customer
    ↓
channel_id
    ↓
dim_channel
```

Therefore, `fact_sales` does not currently contain a direct `channel_id`.

This is an intentional simplification of the simulated Project 1 model.

It assumes that each customer has a primary channel assignment.

### Production consideration

In a production enterprise model, customers may transact through multiple channels.

A future implementation could therefore place the transactional channel directly on the sales fact:

```text
fact_sales
    ├── customer_id
    ├── product_id
    ├── salesperson_id
    └── channel_id
```

This is a potential future enhancement rather than a required change to the current Project 1 architecture.

---

# 10. Geographic Architecture

Aurevia uses a four-level geographic hierarchy:

```text
Global
   ↓
Region
   ↓
Cluster
   ↓
Country
```

## 10.1 Global

Represents the entire Aurevia Group.

## 10.2 Region

Current regions:

- Europe
- North America
- Emerging Markets

## 10.3 Cluster

Management-defined groupings within regions.

Current examples include:

| Region | Cluster | Countries |
|---|---|---|
| Europe | Northern Europe | United Kingdom, Netherlands |
| Europe | Central Europe | Germany |
| Europe | Southern Europe | France, Spain, Italy |
| North America | US & Canada | United States, Canada |
| North America | Mexico | Mexico |
| Emerging Markets | Latin America | Brazil |
| Emerging Markets | South Asia | India |
| Emerging Markets | Southern Africa | South Africa |
| Emerging Markets | Middle East | United Arab Emirates |

## 10.4 Country

Country represents the individual market level.

The geographic implementation is:

```text
dim_region
    │
    └── dim_cluster
            │
            └── dim_country
```

Clusters are management-defined analytical groupings and may evolve as Aurevia's geographic strategy changes.

---

# 11. Fact-Table Grain and Aggregation Rules

Grain is a central architectural principle because incorrect grain handling can produce materially incorrect management information.

## 11.1 Sales

```text
fact_sales
= one product line within one customer order
```

Therefore:

```text
COUNT(*)
```

is not an order count.

Use:

```text
COUNT(DISTINCT order_id)
```

for distinct orders.

---

## 11.2 Returns

```text
fact_returns
= one returned product line associated with an original sales line
```

Returns should be aggregated independently before joining them to sales-level metrics.

---

## 11.3 Targets

```text
fact_targets
= date × division × region × channel
```

Actual sales should be aggregated to the corresponding analytical grain before being joined to target data.

This prevents target values from being duplicated across individual sales transactions.

---

## 11.4 Segment-level order counts

An order may contain multiple products and potentially products from multiple divisions.

Therefore, distinct order counts calculated at a segment level should not automatically be summed to represent enterprise-wide unique orders.

Enterprise-wide order counts should be calculated directly at the enterprise grain:

```text
COUNT(DISTINCT order_id)
```

---

## 11.5 Derived ratios

Ratios such as:

- Gross margin
- Discount rate
- Return rate
- Target attainment
- Variance percentage

should generally be calculated from appropriately aggregated numerator and denominator values.

Row-level percentages should not simply be averaged to produce enterprise-level ratios.

---

# 12. Data Flow Architecture

The Project 1 analytical flow is:

```text
Source / Simulated Business Data
              ↓
          PostgreSQL
              ↓
     SQL Analytical Queries
              ↓
     Validation / Python
              ↓
     Analytical Outputs
              ↓
          Power BI
              ↓
    Executive Decision Brief
              ↓
       Management Action
```

The analytical workflow is:

```text
Business Problem
       ↓
Data Model
       ↓
Performance Measurement
       ↓
SQL Analysis
       ↓
Validation
       ↓
Target / Variance Analysis
       ↓
Executive Reporting
       ↓
Management Decision
```

---

# 13. Data Quality Architecture

Data quality checks should operate at multiple levels.

## 13.1 Structural integrity

Check:

- Missing primary keys
- Duplicate primary keys
- Invalid foreign keys
- Broken relationships
- Unexpected nulls

## 13.2 Transactional integrity

Check:

- Invalid dates
- Non-positive sales quantities
- Non-positive return quantities
- Negative financial values
- Discount values exceeding gross sales
- Net sales exceeding gross sales

## 13.3 Analytical integrity

Check:

- Revenue reconciliation
- Gross-profit reconciliation
- Product-cost reconciliation
- Division totals against enterprise totals
- Regional totals against enterprise totals
- Channel totals against enterprise totals
- Return calculations
- Target-versus-actual joins

## 13.4 Grain validation

Every analytical query should respect the grain of the underlying fact table.

Particular attention should be paid to:

- Sales-to-return joins
- Sales-to-target joins
- Distinct order counts
- Multi-dimensional aggregation

---

# 14. Data Lineage

The principal Project 1 lineage is:

```text
Business Entities
      ↓
Dimension Tables
      ↓
fact_sales / fact_returns / fact_targets
      ↓
SQL Analytical Queries
      ↓
Validated Metrics
      ↓
Executive Reporting
      ↓
Management Decisions
```

For example:

```text
Product
  ↓
dim_product
  ↓
fact_sales
  ↓
Net Revenue
  ↓
Product Performance Analysis
  ↓
Management Action
```

Returns follow a separate path:

```text
Original Sale
  ↓
fact_sales.sales_id
  ↓
fact_returns.sales_id
  ↓
Return Analysis
  ↓
Estimated GP Impact
  ↓
Management Action
```

Targets follow a planning-performance path:

```text
Illustrative Benchmark
  ↓
fact_targets
  ↓
Target vs Actual
  ↓
Variance
  ↓
Root-Cause Analysis
  ↓
Management Action
```

---

# 15. Analytical and Reporting Layer

The data architecture supports several analytical outputs.

## 15.1 SQL analysis

SQL provides the primary analytical layer for:

- Revenue analysis
- Profitability analysis
- Division analysis
- Geographic analysis
- Channel analysis
- Product analysis
- Customer analysis
- Discount analysis
- Returns analysis
- Target-versus-actual analysis

## 15.2 Python

Python can be used for:

- Analytical validation
- Extended analysis
- Statistical analysis
- Visualisation
- Future predictive modelling

## 15.3 Power BI

Power BI provides the reporting and management-visualisation layer.

The intended semantic model should preserve the business definitions and grain rules documented in the Data Dictionary.

## 15.4 Executive reporting

The analytical outputs feed executive decision support, including:

- Performance diagnosis
- Risk identification
- Commercial priorities
- Margin actions
- Geographic decisions
- Customer priorities
- Product decisions

---

# 16. Future-State Data Domains

The following domains form the planned architecture for the wider Aurevia portfolio.

They are **not all implemented in Project 1**.

---

## 16.1 Finance Data Domain

The finance domain supports profitability analysis, cost allocation, budgeting, investment decisions, and cash-flow analysis.

Potential core tables include:

```text
fact_costs
fact_budgets
fact_expenses
fact_cash_flows
fact_investments
```

Future analysis may include:

- Gross profit
- Gross margin
- Contribution
- Operating costs
- Product profitability
- Regional profitability
- Financial performance against targets
- Investment returns
- Cash-flow analysis

---

## 16.2 Pricing Data Domain

The pricing domain captures product pricing, discounts, promotions, and competitive pricing.

Potential core tables include:

```text
fact_product_prices
fact_discounts
fact_promotions
fact_competitor_prices
```

Future analysis may include:

- Discount rates
- Net revenue
- Discount impact on profitability
- Price changes
- Promotion performance
- Pricing-related margin pressure
- Price elasticity

---

## 16.3 Marketing & Customer Data Domain

This domain supports customer segmentation, acquisition, retention, campaign analysis, and experimentation.

Potential core tables include:

```text
dim_customer_segments
fact_campaigns
fact_campaign_exposures
fact_customer_activity
fact_customer_acquisition
fact_customer_retention
fact_experiments
```

---

## 16.4 Operations Data Domain

This domain supports supply chain, inventory, supplier, shipment, and logistics analysis.

Potential core tables include:

```text
dim_supplier
dim_warehouse
fact_purchase_orders
fact_inventory
fact_inventory_movements
fact_shipments
fact_logistics_costs
fact_lead_times
```

---

## 16.5 Market & Macro Data Domain

This domain supports market entry, competitor analysis, market sizing, and macroeconomic assessment.

Potential core tables include:

```text
dim_market
fact_market_size
fact_market_growth
fact_competitor_market_share
fact_macro_indicators
fact_fx_rates
```

---

## 16.6 Risk & Scenarios Data Domain

This domain supports risk identification, scenario modelling, and simulation.

Potential core tables include:

```text
dim_risk_factor
fact_risk_events
dim_scenario
fact_scenario_assumptions
fact_scenario_outcomes
fact_simulation_runs
```

---

## 16.7 Analytics Data Domain

The analytics domain stores analytical outputs generated by SQL, Python, machine learning, and optimization processes.

Potential tables include:

```text
fact_customer_scores
fact_churn_predictions
fact_demand_forecasts
fact_price_elasticity
fact_price_recommendations
fact_inventory_forecasts
fact_risk_scores
fact_investment_scenarios
fact_optimization_results
fact_executive_recommendations
```

Where appropriate, analytical outputs should include:

- Model version
- Run timestamp
- Prediction or recommendation period
- Relevant entity keys
- Validation metadata
- Model-performance information

---

# 17. Cross-Domain Integration Strategy

As the portfolio expands, domains should be connected through shared business entities and standardized dimensions.

Potential shared dimensions include:

```text
Date
Product
Customer
Country
Region
Channel
Division
Market
Supplier
```

The objective is to allow different analytical domains to be connected without duplicating core business definitions.

For example:

```text
Commercial
    │
    ├── Product
    ├── Customer
    ├── Country
    └── Channel
          │
          ▼
Pricing
          │
          ▼
Finance
          │
          ▼
Executive Decision Support
```

Relationships should be validated during implementation rather than assumed solely from conceptual design.

---

# 18. Architecture Evolution Across the Portfolio

The architecture will develop progressively across the eight projects.

| Project | Primary architectural expansion |
|---|---|
| Project 1 | Commercial performance foundation |
| Project 2 | Market and strategic financial modelling |
| Project 3 | Customer and marketing analytics |
| Project 4 | Pricing and revenue optimization |
| Project 5 | Operations and supply chain |
| Project 6 | Investment and risk intelligence |
| Project 7 | Predictive analytics and data platform capabilities |
| Project 8 | Integrated executive decision support |

The projects share the same underlying business universe but introduce new data domains only when required by their analytical objectives.

---

# 19. Current-State vs Future-State Architecture

The distinction between implemented and planned architecture is important.

### Current Project 1 architecture

```text
IMPLEMENTED

Dimensions
    ↓
dim_date
dim_division
dim_region
dim_cluster
dim_country
dim_channel
dim_customer
dim_product
dim_salesperson

Facts
    ↓
fact_sales
fact_returns
fact_targets
```

### Future portfolio architecture

```text
PLANNED / PROGRESSIVE

Commercial
Marketing & Customer
Pricing
Operations
Finance
Market & Macro
Risk & Scenarios
Analytics
```

Future tables should not be represented as implemented merely because they appear in the long-term architecture.

They should be introduced when the relevant project requires them.

---

# 20. Architectural Assumptions and Limitations

The current Project 1 architecture contains several intentional modelling assumptions.

### 20.1 Customer-level channel assignment

Each customer has a primary channel assignment.

The current model therefore derives sales channel through `dim_customer`.

A production model may require transaction-level channel assignment if customers transact through multiple channels.

### 20.2 Synthetic target methodology

`fact_targets` contains illustrative retrospective benchmarks rather than genuine historical management targets, budgets, or forecasts.

### 20.3 Simulated data

The Project 1 dataset is fictional and designed for portfolio demonstration.

The architecture therefore demonstrates analytical modelling and decision-support capability rather than representing Aurevia's real operational systems.

### 20.4 Incremental implementation

The long-term architecture intentionally contains domains that are not yet implemented.

This prevents unnecessary complexity and keeps each project aligned with its defined analytical objectives.

---

# 21. Architecture Governance

As the Aurevia portfolio expands, architectural changes should be evaluated against the following questions:

1. What business question requires the change?
2. What new data entity or event is required?
3. What is the grain of the proposed table?
4. What existing dimensions should it connect to?
5. What primary and foreign keys are required?
6. Could the change create duplicate or ambiguous relationships?
7. How will data quality be validated?
8. How will the change affect existing analytical outputs?
9. Is the table required now or should it remain part of the future-state blueprint?
10. Is the business definition documented in the Data Dictionary?

This ensures that the architecture evolves in response to analytical requirements rather than accumulating tables without a clear business purpose.

---

# 22. Architecture Summary

The Aurevia architecture is designed around a simple principle:

```text
Business Understanding
        ↓
Business Data
        ↓
Structured Data Model
        ↓
Validated Analysis
        ↓
Business Insight
        ↓
Strategic Implication
        ↓
Management Decision
```

Project 1 establishes the commercial performance foundation through:

```text
9 Dimension Tables
        +
3 Fact Tables
        ↓
Sales
Returns
Targets
        ↓
Performance Analysis
        ↓
Executive Decision Support
```

The wider portfolio progressively extends this foundation into:

```text
Commercial
     ↓
Customer & Marketing
     ↓
Pricing
     ↓
Operations
     ↓
Finance
     ↓
Market & Macro
     ↓
Risk & Scenarios
     ↓
Predictive & Advanced Analytics
     ↓
Integrated Executive Decision Support
```

The architecture is therefore designed to evolve from a **well-defined commercial performance model** into an integrated analytical environment capable of supporting strategic, financial, operational, predictive, and executive decision-making.
