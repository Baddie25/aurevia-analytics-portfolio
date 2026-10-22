
# Aurevia Group

> **Data, Strategy, Decision Intelligence & Responsible AI Portfolio**

---

# Project 2 — Market Entry Strategy
## Skincare Competitor and Positioning Framework

### 1. Purpose

This framework establishes a consistent, evidence-led method for evaluating skincare competition across Aurevia's eight candidate markets.

The objective is to understand where Aurevia could compete credibly, which customer needs and product categories matter, how competitors position themselves, and which routes to market may be feasible.

Competitor presence does not establish market attractiveness. The framework therefore does not generate a composite country score or an entry recommendation.

### 2. Decision question

**In which candidate markets, product categories and price positions could Aurevia establish a differentiated and economically viable skincare proposition?**

The research should ultimately inform:
- Market screening and shortlist decisions.
- Product-category and customer-segment selection.
- Brand and price positioning.
- Distribution and route-to-market choices.
- Entry-cost, margin and investment assumptions.
- The final enter, delay or do-not-enter decision.

### 3. Candidate-market universe

Retain all eight markets during the initial research stage:

- Australia — AUS
- Chile — CHL
- Indonesia — IDN
- Japan — JPN
- Poland — POL
- Saudi Arabia — SAU
- South Korea — KOR
- Türkiye — TUR

The initial list is a research universe, not a ranking. Markets should not be removed solely because public competitor information is less accessible.

### 4. Aurevia's relevant product scope

Aurevia's existing catalogue contains three products directly relevant to the initial skincare and adjacent personal-care investigation:

| Existing product | Division | Research category |
|---|---|---|
| Daily Facial Cleanser | Personal Care | Facial cleansers |
| Hydrating Body Wash | Personal Care | Body cleansing and body care |
| Nourishing Hand Cream | Personal Care | Hand care and hand moisturisers |

The facial cleanser is the clearest starting point for a facial-skincare competitive comparison. Body wash and hand cream should be analysed in adjacent categories rather than treated as interchangeable facial-skincare products.

Do not assume Aurevia already sells sunscreen, serums, acne treatments or premium dermocosmetics. These may be investigated as potential expansion categories, clearly labelled as such.

### 5. Research stages

#### Stage A — Define the category

For each observation, establish:
- The product category and subcategory.
- Whether it matches an existing Aurevia product or a possible future extension.
- The customer need or use case.
- Whether the source measures retail sales, wholesale sales, online sales or another basis.

#### Stage B — Identify relevant competitors

Build a longlist of:
- Established multinational brands.
- Local and regional brands.
- Dermatological and pharmacy-led brands.
- Digital-first and social-commerce brands.
- Value-oriented and retailer-owned brands where relevant.

Do not assume every well-known beauty brand competes directly with Aurevia. Record why each brand is relevant to the specific category and target customer.

#### Stage C — Examine positioning

Capture product claims, target customer, ingredient or efficacy proposition, pack size, observed price, price per standard unit, and evidence of differentiation.

#### Stage D — Examine distribution

Investigate:
- Pharmacies and health-and-beauty specialists.
- Supermarkets and general retailers.
- Beauty specialty chains and department stores.
- Local and international e-commerce platforms.
- Brand-owned websites and direct-to-consumer channels.
- Importers, distributors and other potential intermediaries.

A listed online product demonstrates availability on that platform at the observation date; it does not establish national distribution or sales volume.

#### Stage E — Assess commercial implications

Connect verified observations to:
- Target-segment attractiveness.
- Competitor intensity and differentiation.
- Achievable price positioning.
- Distribution access and partner requirements.
- Regulatory and localisation requirements.
- Indicative costs, margins and entry economics.

Do not infer market share, demand, profitability or consumer preference from product listings alone.

### 6. Competitor evidence register

Maintain one structured observation per source-backed finding in:

`data/external/skincare_competitor_landscape_evidence.csv`

Capture:
- Evidence ID and country.
- Brand or company.
- Product category and product name where applicable.
- Observation type and observed value.
- Currency, pack size and standardised price where relevant.
- Channel and observation date.
- Source title, organisation and URL.
- Evidence tier, limitations and verification status.

Use one row per observation rather than combining several brands or prices into a single free-text cell.

### 7. Price-comparison rules

Price comparisons should only be made between reasonably comparable products.

1. Record the original listed price and local currency.
2. Record pack size and unit of measurement.
3. Calculate price per 100 ml or 100 g where appropriate.
4. Record promotional and regular prices separately when both are visible.
5. Capture the retailer, URL and date observed.
6. Record whether taxes, shipping or import charges are included when known.
7. Do not convert currencies until the original local-currency price is preserved.
8. Do not compare a promotional price in one market with an undiscounted price in another without flagging the difference.

A small convenience pack and a large refill pack should not be compared using headline price alone.

### 8. Evidence hierarchy

**Tier 1 — Primary or authoritative**
- Official brand and retailer product listings.
- Company filings and official company statements.
- Government or regulatory sources for legal and product requirements.
- Directly accessible, clearly defined market data from authoritative institutions.

**Tier 2 — Established market research**
- Country-specific Euromonitor, Circana, NielsenIQ or comparable research where the methodology and category definition are sufficiently clear.
- Reputable industry studies with identifiable observation periods and metrics.

**Tier 3 — Reputable trade and business press**
- Useful for brand launches, channel developments and emerging competitor signals.
- Verify important claims against primary or stronger secondary evidence where possible.

**Tier 4 — Discovery only**
- Search snippets, influencer content, unverified social posts and unsupported marketplace rankings.
- Use to identify leads, not to establish market share or make investment claims.

A source tier does not eliminate the need to check definitions, dates, geographic coverage and limitations.

### 9. Verification statuses

Use consistent labels:
- `Verified` — directly checked against the cited source.
- `Partially verified` — the source supports the broad claim but not all relevant details.
- `Unverified lead` — requires further checking.
- `Not accessible` — a relevant source is identified but its evidence cannot be inspected.
- `Not comparable` — a figure exists but uses a materially different definition or basis.
- `Research gap` — required evidence has not been obtained.

Do not treat inaccessible evidence as zero or as proof of weak market attractiveness.

### 10. Market-level research priorities

| Market | Initial research emphasis |
|---|---|
| Australia | Multinational skincare, Asian-beauty brands, clinical positioning and beauty-specialist e-commerce |
| Chile | Local and international brands, pharmacy distribution, K-beauty availability and mass-versus-premium positioning |
| Indonesia | Local brands, value pricing, digital-first brands, marketplaces and distribution reach |
| Japan | Domestic manufacturers, science-backed formulations, facial-care segments and specialist retail |
| Poland | Local and multinational brands, dermocosmetics, health-and-beauty specialists and K-beauty |
| Saudi Arabia | Pharmacy and beauty-specialist channels, climate-relevant product needs, digital discovery and localisation |
| South Korea | Domestic innovators, ingredient-led differentiation, specialist retail and competitive intensity |
| Türkiye | Domestic and international manufacturers, price architecture, inflation exposure and distribution feasibility |

These are research priorities based on preliminary public evidence, not final strategic conclusions.

### 11. Research controls

- Record the observation date, not just the publication date.
- Preserve source URLs and exact source titles.
- Keep source evidence separate from analyst interpretation.
- Label estimates, assumptions and hypotheses explicitly.
- Do not infer consumer demand from social-media attention alone.
- Do not infer national distribution from a single retailer listing.
- Do not treat company-level market share as brand-level share.
- Do not combine market-size estimates from different publishers until category definitions and currency methods have been reconciled.
- Do not expose confidential company information to external AI tools.

### 12. Output and decision gate

The research stage is complete only when it provides:
1. A traceable competitor longlist for all eight candidate markets.
2. Comparable observations for the most relevant Aurevia product categories.
3. An initial price-positioning comparison with original currencies and pack sizes preserved.
4. A channel map and identified route-to-market questions.
5. An explicit list of unresolved evidence gaps.
6. A reasoned assessment of which markets merit deeper research.

Only then should Aurevia proceed to a more focused shortlist and market-entry economics.

### 13. Current limitations

The initial public-source review identifies competitor signals but does not yet establish:
- Complete brand-level market shares across all eight markets.
- Comparable current prices across equivalent products.
- Verified national distribution coverage.
- Consumer willingness to pay for Aurevia's proposed proposition.
- Aurevia's achievable market share, contribution margin or entry returns.

These remain research tasks, not assumed facts.
