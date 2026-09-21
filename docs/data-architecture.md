
# Aurevia Group — Data Architecture

## 1. Purpose

This document defines the data architecture for Aurevia Group's analytics portfolio.

The architecture supports business performance analysis, strategic decision-making, financial modelling, customer analytics, pricing, supply chain management, risk analysis, and executive reporting.

## 2. Data Architecture Principles

- Use a consistent business vocabulary.
- Define the grain of every fact table.
- Use primary and foreign keys to maintain relationships.
- Separate transactional data from analytical outputs.
- Document assumptions and data lineage.
- Validate data before using it for decision-making.
- Build the data universe incrementally across projects.

## 3. Major Data Domains

| Domain | Purpose |
|---|---|
| Commercial | Sales, customers, products, orders, channels |
| Marketing & Customer | Campaigns, customer activity, retention, experiments |
| Pricing | Prices, discounts, promotions, competitor prices |
| Operations | Suppliers, inventory, shipments, logistics |
| Finance | Costs, budgets, expenses, investments, cash flow |
| Market & Macro | Market size, competitors, economic indicators |
| Risk & Scenarios | Risk factors, scenarios, simulation outputs |
| Analytics | Forecasts, predictions, recommendations, scores |

## 4. Commercial Data Domain

The commercial domain captures Aurevia's sales activity and organizational dimensions.

### 4.1 Dimension Tables

- dim_date
- dim_customer
- dim_product
- dim_division
- dim_country
- dim_region
- dim_channel
- dim_salesperson

### 4.2 Fact Tables

- fact_sales
- fact_returns
- fact_targets

## 5. Fact Table Grain

### fact_sales

One record represents one product line within one customer order.

Example:

An order containing three different products produces three fact_sales records.

This grain supports analysis by:

- Order
- Customer
- Product
- Division
- Country
- Region
- Channel
- Date

### fact_returns

One record represents a returned product line associated with a customer order.

### fact_targets

One record represents a performance target for a defined period and organizational dimension.

## 6. Key Relationships

- dim_customer connects to fact_sales through customer_key.
- dim_product connects to fact_sales through product_key.
- dim_date connects to fact_sales through date_key.
- dim_channel connects to fact_sales through channel_key.
- dim_country connects to fact_sales through country_key.
- dim_region connects to fact_sales through region_key.
- dim_division connects to dim_product through division_key.

## 7. Initial Project 1 Scope

Project 1 will initially use:

- dim_date
- dim_customer
- dim_product
- dim_division
- dim_country
- dim_region
- dim_channel
- dim_salesperson
- fact_sales
- fact_returns
- fact_targets

The initial scope may be expanded when analytical requirements justify additional tables.

## 8. Data Flow

Raw Data
→ PostgreSQL
→ SQL and Python Analysis
→ Analytical Tables
→ Power BI
→ Executive Decision Brief
→ Management Action

## 9. Data Quality Requirements

Before analysis, we will check:

- Missing primary keys
- Duplicate records
- Invalid foreign keys
- Missing dates
- Negative or invalid financial values
- Inconsistent category names
- Unexpected sales and return patterns
- Reconciliation of key financial measures

## 10. Architecture Evolution

The architecture will be developed progressively.

Project 1 establishes the commercial and performance foundation. Subsequent projects will add customer, marketing, pricing, operations, finance, market, risk, and advanced analytics capabilities.


## 11. Finance Data Domain

The finance domain supports profitability analysis, cost allocation, budgeting, investment decisions, and cash-flow analysis.

### 11.1 Core Tables

- fact_costs
- fact_budgets
- fact_expenses
- fact_cash_flows
- fact_investments

### 11.2 Project 1 Relevance

Finance data will help evaluate:

- Gross profit
- Gross margin
- Contribution
- Operating costs
- Product profitability
- Regional profitability
- Financial performance against targets

## 12. Pricing Data Domain

The pricing domain captures product pricing, discounts, promotions, and price changes.

### 12.1 Core Tables

- fact_product_prices
- fact_discounts
- fact_promotions
- fact_competitor_prices

### 12.2 Project 1 Relevance

Pricing data will help evaluate:

- Discount rates
- Net revenue
- Discount impact on profitability
- Product price changes
- Promotion performance
- Pricing-related margin pressure

## 13. Initial Analytical Relationships

The commercial, finance, and pricing domains will be connected through shared business keys, including:

- Date
- Product
- Customer
- Country
- Region
- Channel
- Division

Relationships will be validated during schema implementation and data-quality testing.


## 14. Marketing & Customer Data Domain

This domain supports customer segmentation, acquisition, retention, campaign performance, and experimentation.

### Core Tables

- dim_customer_segments
- fact_campaigns
- fact_campaign_exposures
- fact_customer_activity
- fact_customer_acquisition
- fact_customer_retention
- fact_experiments

## 15. Operations Data Domain

This domain supports supply chain, inventory, supplier, shipment, and logistics analysis.

### Core Tables

- dim_supplier
- dim_warehouse
- fact_purchase_orders
- fact_inventory
- fact_inventory_movements
- fact_shipments
- fact_logistics_costs
- fact_lead_times

## 16. Market & Macro Data Domain

This domain supports market entry, competitor analysis, market sizing, and macroeconomic assessment.

### Core Tables

- dim_market
- fact_market_size
- fact_market_growth
- fact_competitor_market_share
- fact_macro_indicators
- fact_fx_rates

## 17. Risk & Scenarios Data Domain

This domain supports risk identification, scenario modelling, and simulation.

### Core Tables

- dim_risk_factor
- fact_risk_events
- dim_scenario
- fact_scenario_assumptions
- fact_scenario_outcomes
- fact_simulation_runs

## 18. Analytics Data Domain

This domain stores analytical outputs generated by SQL, Python, machine learning, and optimization processes.

### Core Tables

- fact_customer_scores
- fact_churn_predictions
- fact_demand_forecasts
- fact_price_elasticity
- fact_price_recommendations
- fact_inventory_forecasts
- fact_risk_scores
- fact_investment_scenarios
- fact_optimization_results
- fact_executive_recommendations

Analytical tables will include model versions, timestamps, and relevant validation metadata where appropriate.

## 19. Architecture Implementation Strategy

The complete architecture provides a long-term blueprint for all eight projects.

Implementation will be incremental:

1. Project 1: Commercial, finance, and pricing foundations.
2. Project 2: Market and financial modelling.
3. Project 3: Customer and marketing analytics.
4. Project 4: Pricing and revenue optimization.
5. Project 5: Operations and supply chain.
6. Project 6: Investment and risk intelligence.
7. Project 7: Predictive platform and data engineering.
8. Project 8: Integrated executive decision support.

Only the tables required for each project's defined analytical objectives will be implemented at that stage.



## Geographic Hierarchy

Aurevia Group uses a four-level geographic hierarchy:

Global → Region → Cluster → Country

This structure allows management to analyze performance at different levels of geographic detail.

### Hierarchy

- **Global:** Aurevia Group
- **Region:** Europe, North America, Emerging Markets
- **Cluster:** Management-defined geographic groupings within each region
- **Country:** Individual operating markets

### Example

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

### Database Implementation

The geographic hierarchy is implemented through:

- `dim_region`
- `dim_cluster`
- `dim_country`

Relationships:

```text
dim_region
    |
    └── dim_cluster
            |
            └── dim_country
```

The `dim_country` table contains a foreign key to `dim_cluster`, while `dim_cluster` contains a foreign key to `dim_region`.

Clusters are management-defined analytical groupings and may be revised as Aurevia's geographic strategy evolves.