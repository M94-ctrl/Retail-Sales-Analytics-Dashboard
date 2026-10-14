
import pandas as pd

s = pd.read_csv("data/Sales.csv", parse_dates=["OrderDate"])
c = pd.read_csv("data/Customers.csv")
p = pd.read_csv("data/Products.csv")
st = pd.read_csv("data/Stores.csv")

print("== Row counts ==")
for n, d in [("Sales", s), ("Customers", c), ("Products", p), ("Stores", st)]:
    print(f"{n:10s}{len(d):>6}")

print("\n== Quality checks ==")
print("Missing values in Sales      :", int(s.isna().sum().sum()))
print("Duplicate Sales rows         :", int(s.duplicated().sum()))
print("Orphan CustomerID            :", int((~s.CustomerID.isin(c.CustomerID)).sum()))
print("Orphan ProductID             :", int((~s.ProductID.isin(p.ProductID)).sum()))
print("Orphan StoreID               :", int((~s.StoreID.isin(st.StoreID)).sum()))
print("Quantity <= 0                :", int((s.Quantity <= 0).sum()))
print("Discount outside 0/5/10/15 % :", int((~s.DiscountPct.isin([0, .05, .1, .15])).sum()))
print("Unit cost >= unit price      :", int((p.UnitCost >= p.UnitPrice).sum()))
print("Date range                   :", s.OrderDate.min().date(), "to", s.OrderDate.max().date())

d = s.merge(p, on="ProductID").merge(st, on="StoreID")
d["Gross"] = d.Quantity * d.UnitPrice
d["Net"] = d.Gross * (1 - d.DiscountPct)
d["Profit"] = d.Net - d.Quantity * d.UnitCost

print("\n== Headline KPIs ==")
print(f"Total Sales (net revenue): {d.Net.sum():,.2f}")
print(f"Total Profit             : {d.Profit.sum():,.2f}")
print(f"Profit margin            : {d.Profit.sum() / d.Net.sum():.1%}")
print(f"Orders                   : {s.OrderID.nunique():,}")
print(f"Active customers         : {s.CustomerID.nunique():,}")
print("\nNet sales by year:\n", d.groupby(d.OrderDate.dt.year).Net.sum().round(2).to_string())
