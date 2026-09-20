
# Aurevia Group — Data Dictionary

## Project 1: Enterprise Performance Command Center

### Purpose

Define the business metrics, dimensions, and analytical fields required to evaluate Aurevia Group's commercial and financial performance from 2022 to 2026.

Metrics must have clear definitions, calculation rules, business interpretations, and appropriate aggregation levels.

---

## 1. Core Financial KPIs

| KPI | Definition | Formula | Business Interpretation |
|---|---|---|---|
| Revenue | Total value of products sold before discounts and returns | Sum of gross sales value | Measures commercial scale |
| Discount Amount | Total value reduced through discounts | Gross Revenue - Net Revenue before returns | Measures discount impact |
| Net Revenue | Revenue after discounts | Gross Revenue - Discount Amount | Measures realized sales revenue |
| Product Cost | Direct cost associated with products sold | Sum of product costs | Measures direct cost base |
| Gross Profit | Net revenue less product cost | Net Revenue - Product Cost | Measures profit before operating costs |
| Gross Margin | Gross profit as a percentage of net revenue | Gross Profit / Net Revenue | Measures profitability of sales |
| Orders | Number of unique customer orders | Count of distinct order IDs | Measures transaction volume |
| Units Sold | Total quantity of products sold | Sum of quantity | Measures product volume |
| Average Order Value | Average net revenue per order | Net Revenue / Orders | Measures order economics |

---

## 2. Growth KPIs

| KPI | Definition | Formula | Business Interpretation |
|---|---|---|---|
| Revenue Growth | Percentage change in revenue over time | (Current Revenue - Previous Revenue) / Previous Revenue | Measures sales expansion |
| Gross Profit Growth | Percentage change in gross profit | (Current GP - Previous GP) / Previous GP | Measures profit expansion |
| Target Attainment | Actual performance compared with target | Actual / Target | Measures performance against plan |
| Revenue per Customer | Average net revenue generated per customer | Net Revenue / Active Customers | Measures customer value |

---

## 3. Commercial Dimensions

Performance should be analyzed across:

- Date
- Year
- Month
- Division
- Product
- Product Category
- Customer
- Customer Segment
- Country
- Region
- Channel
- Salesperson

---

## 4. Analytical Requirements

Each KPI must be evaluated by:

1. Overall company performance
2. Year-over-year change
3. Division
4. Region
5. Country
6. Channel
7. Product category
8. Customer segment

### Validation Requirements

- Revenue must reconcile with underlying sales records.
- Net revenue must account for discounts.
- Gross profit must reconcile with product costs.
- Division, region, and channel totals must reconcile with company totals.
- Missing or invalid financial values must be investigated.
- KPI definitions must remain consistent across SQL, Python, and Power BI.

---

## 5. Scope Boundary

Project 1 focuses on descriptive and diagnostic analytics.

Predictive modelling, optimization, advanced experimentation, and automated decision systems will be developed in later projects.