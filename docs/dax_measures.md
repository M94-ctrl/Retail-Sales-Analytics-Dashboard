# DAX Measures (from `Sales_Dashboard.pbix`)

## Overview
```DAX
Total Sales      = SUM('Sales'[Net revenue])
Total Profit     = SUM(Sales[Profit])
Number of Order  = DISTINCTCOUNT(Sales[OrderID])
Unique Customers = DISTINCTCOUNT(Sales[CustomerID])
Profit Margin %  = DIVIDE([Total Profit], [Total Sales])
Sales Last Year  = CALCULATE(SUM(Sales[Net revenue]), DATEADD('Date Table'[Date], -1, YEAR))
YoY Growth %     = DIVIDE(SUM(Sales[Net revenue]) - [Sales Last Year], [Sales Last Year])
```

## Time analysis
```DAX
Sales YTD           = IF(NOT ISBLANK([Total Sales]), TOTALYTD([Total Sales], 'Date Table'[Date]))
Sales YTD Last Year = CALCULATE([Sales YTD], SAMEPERIODLASTYEAR('Date Table'[Date]))
Sales Last Year1    = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date Table'[Date]))
Rolling 3 Month     = IF(NOT ISBLANK([Total Sales]),
                        CALCULATE([Total Sales], DATESINPERIOD('Date Table'[Date], MAX('Date Table'[Date]), -3, MONTH)))
MoM Growth %        = VAR Curr = [Total Sales]
                      VAR Prev = CALCULATE([Total Sales], DATEADD('Date Table'[Date], -1, MONTH))
                      RETURN IF(NOT ISBLANK(Curr), DIVIDE(Curr - Prev, Prev))
Month Best Sales    = MAXX(VALUES('Date Table'[Month]), [Total Sales])
Best Month Name     = VAR BestValue = [Month Best Sales]
                      RETURN CALCULATE(MAX('Date Table'[Month]),
                               FILTER(VALUES('Date Table'[Month]), [Total Sales] = BestValue))
```

## Product & region
```DAX
% Share              = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Products[ProductName])))
% of Orders          = DIVIDE(DISTINCTCOUNT(Sales[OrderID]), CALCULATE(DISTINCTCOUNT(Sales[OrderID]), ALL(Stores)))
Growth %             = VAR new = [Total Sales]
                       VAR old = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date Table'[Date]))
                       RETURN IF(HASONEVALUE('Date Table'[Year]) && NOT ISBLANK(new), DIVIDE(new - old, old))
% of total sales     = CALCULATE([Total Sales], ALLEXCEPT(Stores, Stores[Region]))
Total Sales Share %  = DIVIDE([Total Sales], CALCULATE([Total Sales], ALLSELECTED(Stores[Region])))
```

## Customer
```DAX
Unique Customer        = DISTINCTCOUNT(Sales[CustomerID])
Avg Sales per Customer = DIVIDE([Total Sales], DISTINCTCOUNT(Sales[CustomerID]))
Large order %          = DIVIDE(CALCULATE(DISTINCTCOUNT(Sales[OrderID]), Sales[Quantity] > 3), DISTINCTCOUNT(Sales[OrderID]))
% of Total Sales1      = DIVIDE([Total Sales], CALCULATE([Total Sales], ALLSELECTED(Sales[CustomerID])))
Sales 2024             = CALCULATE(SUM(Sales[Net revenue]), 'Date Table'[Year] = 2024)
Sales 2025             = CALCULATE(SUM(Sales[Net revenue]), 'Date Table'[Year] = 2025)
Growth_%               = VAR S24 = [Sales 2024] VAR S25 = COALESCE([Sales 2025], 0)
                         RETURN IF(NOT ISBLANK(S24), DIVIDE(S25 - S24, S24))
```
> "Large order %" counts orders that have **at least one line** with quantity > 3.

## Pareto (top customers)
```DAX
Top Percent Value     = SELECTEDVALUE('Top Percent'[Top Percent], 0.2)
Number of Top Customers = ROUNDUP(DISTINCTCOUNT(Sales[CustomerID]) * [Top Percent Value], 0)
Top Customer Share    = VAR Top_Count = [Number of Top Customers]
                        VAR TopSales  = SUMX(TOPN(Top_Count, VALUES(Sales[CustomerID]), [Total Sales], DESC), [Total Sales])
                        RETURN DIVIDE(TopSales, [Total Sales])
Customer Rank         = IF(HASONEVALUE(Customers[CustomerID]) && NOT ISBLANK([Total Sales]),
                           RANKX(ALLSELECTED(Customers), [Total Sales], , DESC, Dense))
Cumulative %          = VAR CurrentSales = [Total Sales]
                        VAR CumSales = SUMX(FILTER(ALLSELECTED(Customers), [Total Sales] >= CurrentSales), [Total Sales])
                        VAR AllSales = CALCULATE([Total Sales], ALLSELECTED(Customers))
                        RETURN IF(HASONEVALUE(Customers[CustomerID]) && NOT ISBLANK(CurrentSales), DIVIDE(CumSales, AllSales))
```

## Review notes
- `Unique Customers` and `Unique Customer` are duplicates; `Top Percent Value` and `Top Percent Value 2` are duplicates; `Sales Last Year` and `Sales Last Year1` use different time functions for the same idea. Consolidating them makes the model easier to maintain.
- `Growth_%` compares 2025 (to 29 Nov) with full-year 2024.
