# 🛒 Retail Sales Analytics Dashboard

A 6-page interactive **Power BI** dashboard for a multi-store retail business: sales and profit performance, customer value (Pareto / top-20% analysis), product and region mix, and time-based trends (YoY, MoM, YTD, rolling 3-month).

**Tools:** Power BI · DAX · Power Query (M) · Data modelling · Python (validation script)

---

## 📌 Business Questions
- How much are we selling and how profitable is it (by category, product, store, region)?
- Which customers drive most of the revenue? Do the top 20% of customers generate ~80%?
- How are sales trending year-over-year and month-over-month, and what is the seasonality?
- Which stores and products deserve attention?

## 📊 Dashboard Pages
| Page | What it shows |
|---|---|
| **Overview** | KPI cards (Total Sales, Total Profit, YoY Growth %, Orders, Unique Customers), sales vs last year by month, sales by store, sales & profit by category, sales by region; slicers for Year and Region |
| **Customer Analysis** | Avg sales per customer, unique customers, large-order %, sales by segment, top customers, 2024 vs 2025 growth per customer, each customer's share of total sales; slicers for Year and Segment |
| **Top 20% Customers (Pareto Analysis)** | Adjustable "Top Percent" slicer (5%–50%), Number of Top Customers, Top Customer Share, sales + cumulative % curve, customer ranking table |
| **Product & Region Analysis** | Product share of sales, profit margin by category, sales by product and store, region table (share of sales, share of orders, growth %), category × region matrix |
| **Top 5 Analysis** | Top-5 products, customers and cities by sales, filterable by Year, Region, Store, Segment, City and Category |
| **Time Analysis** | Sales YTD vs last-year YTD, rolling 3-month sales, MoM growth %, best month, monthly sales; slicers for Year and Region |

### Screenshots
| | |
|---|---|
| ![Overview](docs/screenshots/overview.png) | ![Customer Analysis](docs/screenshots/customer_analysis.png) |
| ![Top 20% Customers](docs/screenshots/top_20_customers_pareto.png) | ![Product and Region](docs/screenshots/product_and_region_analysis.png) |
| ![Top 5 Analysis](docs/screenshots/top_5_analysis.png) | ![Time Analysis](docs/screenshots/time_analysis.png) |

## 🔑 Key Results (Jan 2023 – 29 Nov 2025)
| KPI | Value |
|---|---|
| Net sales | **187,280** |
| Profit | **77,884** (margin **41.6%**) |
| Orders / order lines | 1,170 / 1,609 |
| Active customers | 123 (of 150 in the customer list) |

**Insights**
- **Growth:** net sales rose from 53.0K (2023) to 66.7K (2024), **+25.7%**. 2025 is at 67.6K with December missing, so it is already ahead of full-year 2024 (+1.4%).
- **Electronics is the volume leader but the low-margin line:** 39.9% of sales but only **25.8% margin**, vs **62.0%** for Stationery and **51.4%** for Accessories. Pushing accessories alongside electronics is the clearest margin lever.
- **Customer concentration:** the top 20% of buying customers (25 of 123) generate **63.8%** of sales — a strong but less extreme Pareto than the classic 80/20.
- **Regions are balanced** (West 26.0%, North 25.9%, East 24.1%, South 23.9%); **Delhi Central** (16.3%), **Mumbai Plaza** (15.6%) and **Kolkata Hub** (15.1%) are the top stores.
- **Seasonality:** November is the strongest month (21.7K across the three years), followed by December and October.
- **Discounting:** 64% of order lines carry no discount; the rest are 5%, 10% or 15%.

## 🧱 Data Model (star schema)
```
Customers ─┐
Products  ─┼──< Sales (fact) >── Stores
           │
Date Table (calendar 2023-2025)      Top Percent (what-if parameter, 5%–50%)
```
Full details: [`docs/data_model.md`](docs/data_model.md) · All DAX measures: [`docs/dax_measures.md`](docs/dax_measures.md)

### Power Query transformations on `Sales`
Discount % (0.05 → 5), join to Products for UnitCost / UnitPrice, then
`Gross revenue = Quantity × UnitPrice` → `Discount Value` → `Net revenue = Gross − Discount` → `Profit = Net − Quantity × UnitCost`.

## ✅ Data Quality
The raw files are clean — 0 missing values, 0 duplicates, 0 orphan keys, all discounts in {0, 5, 10, 15}%, no product sold below cost. Run `python scripts/validate_data.py` to reproduce the checks and headline KPIs.

## 📁 Repository Structure
```
Retail-Sales-Analytics-Dashboard/
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   ├── Sales.csv          # 1,609 order lines (2023-2025)
│   ├── Customers.csv      # 150 customers
│   ├── Products.csv       # 25 products
│   └── Stores.csv         # 8 stores
├── powerbi/Sales_Dashboard.pbix
├── scripts/validate_data.py
└── docs/
    ├── data_model.md
    ├── dax_measures.md
    └── screenshots/
```

## ▶️ How to Run
1. Open `powerbi/Sales_Dashboard.pbix` in Power BI Desktop (Windows).
2. The file points to `C:\Users\client\Desktop\retail_dataset\*.csv`. Go to **Transform data → Data source settings → Change Source** and select the CSVs in this repo's `data/` folder.
3. Click **Refresh**.

## 🔭 Possible Next Steps
Add a Customer dimension attribute for city-level maps, add a Date → Sales relationship check (see data_model.md), compare Electronics margin by supplier/brand, and add forecasting for the missing December 2025.

## 👤 Author
**Mushtaque Ahmad** — [GitHub](https://github.com/M94-ctrl) · [LinkedIn](https://linkedin.com/in/mushtaque-ahmad-2863aa224)

*The dataset is synthetic and used for portfolio purposes. Currency is not specified in the source data, so values are shown as plain numbers.*
