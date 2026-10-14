# Data Model

## Source tables (CSV)
| Table | Rows | Columns |
|---|---|---|
| Sales | 1,609 | OrderLineID, OrderID, OrderDate, CustomerID, ProductID, StoreID, Quantity, DiscountPct |
| Customers | 150 | CustomerID, CustomerName, City, Segment (Consumer / Corporate / Small Business), JoinDate |
| Products | 25 | ProductID, ProductName, Category, SubCategory, UnitCost, UnitPrice |
| Stores | 8 | StoreID, StoreName, City, Region (North / South / East / West) |

## Calculated tables
- `Date Table = CALENDAR(DATE(2023,01,01), DATE(2025,12,31))` with columns Month number, Month (`MMM`), Year.
- `Top Percent = GENERATESERIES(0.05, 0.5, 0.05)` — what-if parameter that drives the Pareto page.

## Relationships (many-to-one, single direction)
- `Sales[CustomerID]` → `Customers[CustomerID]`
- `Sales[ProductID]` → `Products[ProductID]`
- `Sales[StoreID]` → `Stores[StoreID]`

> ⚠️ **Check:** the model metadata lists no relationship between `Date Table[Date]` and `Sales[OrderDate]`. The time-intelligence measures (YTD, MoM, YoY, rolling 3-month) need that relationship to filter correctly. If it is missing in Power BI's Model view, add `Date Table[Date]` → `Sales[OrderDate]` (many-to-one).

## Columns added in Power Query (`Sales`)
| Column | Logic |
|---|---|
| Discount % | `DiscountPct` mapped to 5 / 10 / 15 / 0 |
| UnitCost, UnitPrice | merged from `Products` on ProductID |
| Gross revenue | `Quantity × UnitPrice` |
| Discount Value | `Discount % × Gross revenue / 100` |
| Net revenue | `Gross revenue − Discount Value` |
| Profit | `Net revenue − Quantity × UnitCost` |

> The Power Query step maps only 0.05 / 0.10 / 0.15 to a discount; any other value would silently become 0%. The current data contains only those values.

## Data notes
- Orders cover 3 Jan 2023 – 29 Nov 2025, so **2025 is a partial year**; YoY and 2024-vs-2025 measures understate 2025.
- 27 of the 150 customers have no purchases.
