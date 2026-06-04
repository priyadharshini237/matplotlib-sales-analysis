import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
supermarket = pd.read_csv('superstore_data.csv', encoding='latin1')
hd = supermarket.head()
print(hd)
ds = supermarket.describe()
print(ds)
supermarket.info()
sh = supermarket.shape
print(sh)
vc = supermarket["Category"].value_counts()
print(vc)
supermarket["Order Date"] = pd.to_datetime(supermarket["Order Date"])
supermarket["Ship Date"] = pd.to_datetime(supermarket["Ship Date"])
yearly_sales = supermarket.groupby(supermarket["Order Date"].dt.to_period("Y")) ["Sales"].sum()
print(yearly_sales)
ship_quantity = supermarket.groupby("Ship Mode")["Quantity"].sum()
print(ship_quantity)
country_cate = pd.pivot_table (
    supermarket,
    index = "City",
    columns = "Category",
    values = "Sales",
    aggfunc = "sum"
)
print(country_cate)
dis_vs_pro = supermarket[["Discount", "Profit"]].corr()
print(dis_vs_pro)
top_10_products = supermarket.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10)
print(top_10_products)
quantity_vise_sales = supermarket[["Sales", "Quantity"]].corr()
print(quantity_vise_sales)
supermarket['Delivery Days'] = (supermarket['Ship Date'] - supermarket['Order Date']).dt.days
print(supermarket['Delivery Days'])
plt.figure(figsize=(8,5))
plt.bar(supermarket["Category"], supermarket["Quantity"], color = 'purple', label = 'Region')
plt.legend()
plt.title("Category vise Quantity")
plt.savefig("category_quantity.png", dpi=300, bbox_inches='tight')
plt.show()

#Region-wise Profit
plt.figure(figsize=(8,5))
plt.bar(supermarket["Region"], supermarket["Profit"], color= "green", label = 'Region')
#plt.title("Region-wise Profit")
plt.xlabel("Region")
plt.ylabel("Profit")
plt.legend()
plt.savefig("region_profit.png", dpi=300, bbox_inches='tight')
plt.show()

#Yearly Sales Trend
plt.figure(figsize=(8,5))
yearly_sales.index = yearly_sales.index.to_timestamp()
plt.plot(yearly_sales.index, yearly_sales.values)
plt.title('Yearly Sales Trend')
plt.xlabel('Years')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.savefig("yearly_sales.png", dpi=300, bbox_inches='tight')
plt.show()

#Top 10 Products by Sales
plt.figure(figsize=(8,5))
plt.barh(top_10_products.index, top_10_products.values, color='purple', edgecolor = 'black')
plt.title('Top 10 sales products')
plt.xlabel('Sub category')
plt.ylabel('Sales')
plt.gca().invert_yaxis()
plt.savefig('top_10_products.png')
plt.show()

#Sales Distribution
plt.figure(figsize=(8,5))
plt.hist(supermarket['Sales'], bins=30, color='yellow')
plt.title('Sales Distribution')
plt.savefig('Sales distribution.png')
plt.show()

#Is higher discount reducing profit?
plt.figure(figsize=(8,5))
plt.scatter(supermarket['Discount'], supermarket['Profit'], color='green', edgecolor='black')
plt.title('Discount vs Profit')
plt.xlabel('Discount')
plt.ylabel('Profit')
plt.axhline(0)
plt.savefig('Discount vs Profit.png')
plt.show()

#Ship Mode Analysis
plt.figure(figsize=(8,5))
supermarket['Delivery_time'] = (supermarket["Ship Date"] - supermarket["Order Date"]).dt.days
avrg_delivery = supermarket.groupby('Ship Mode')['Delivery_time'].mean()
plt.bar(avrg_delivery.index, avrg_delivery.values, color='silver', edgecolor='gold', label='avrg_delivery')
plt.title("Ship mode analysis")
plt.xlabel('Ship Mode')
plt.ylabel('Delivery Time')
plt.legend()
plt.savefig('Ship mode analysis.png')
plt.show()

#Sub-Category Performance
plt.figure(figsize=(8,5))
sales_subcategory = supermarket.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
plt.bar(sales_subcategory.index, sales_subcategory.values, color='pink' , edgecolor='black')
plt.xticks(rotation=45)
plt.title('Category Performance')
plt.xlabel('Sub Category')
plt.ylabel('Sales')
plt.savefig('Category Performances.png')
plt.show()

#City-wise Top Sales
plt.figure(figsize=(8,5))
top_10_cities = supermarket.groupby("City")['Sales'].sum().sort_values(ascending=False).head(10)
plt.barh(top_10_cities.index, top_10_cities.values, color='salmon', label='top_10_cities')
plt.title('Top 10 cities')
plt.xlabel('Sales')
plt.ylabel('City')
plt.legend()
plt.savefig('City-Wise Top Sales.png')
plt.show()

#Profit Trend Over Time
plt.figure(figsize=(8,5), facecolor='pink')
profit_months = supermarket.groupby(supermarket["Order Date"].dt.to_period('M'))['Profit'].sum()
profit_months.index = profit_months.index.to_timestamp()
plt.plot(profit_months.index, profit_months.values, color='lime')
plt.gca().set_facecolor('lightyellow')
plt.title('Profit Trend Over Time', color='black')
plt.xlabel('Months', color='black')
plt.ylabel('Profit', color='black')
plt.savefig('Monthly_profit.png')
plt.show()

#11. Dual Axis Chart
monthly_chart = supermarket.groupby(supermarket["Order Date"].dt.to_period('M')).agg({
    'Sales' : np.sum,
    'Profit' : np.sum
})
monthly_chart.index = monthly_chart.index.to_timestamp()
fig, ax1 = plt.subplots(figsize=(10,5), facecolor = 'lightblue')
ax1.plot(monthly_chart.index, monthly_chart['Sales'], marker='s', color='purple')
ax1.set_xlabel('Months')
ax1.set_ylabel('Sales')
ax2 = ax1.twinx()
ax2.plot(monthly_chart.index, monthly_chart['Profit'], marker='s', color='green')
ax2.set_xlabel('Months')
ax2.set_ylabel('Profit')
plt.title('Sales vs Profit Trend')
plt.xticks(rotation=45)
plt.savefig('Dual Axis chart.png')
plt.show()

#Loss vs Profit Visualization
colors = supermarket['Profit'].apply(lambda x : 'green' if x > 0 else 'red' )
plt.figure(figsize=(8,5), facecolor='lightyellow')
plt.bar(range(len(supermarket)), supermarket['Profit'], color=colors)
plt.title('Profit vs Loss Visualization')
plt.xlabel('Orders')
plt.ylabel('Profit')
plt.savefig('supermarket_profit_vs_loss.png')
plt.show()

#Category-wise sales split by region.
pivot_data = supermarket.pivot_table(
    index = "Category",
    values = "Sales",
    columns = "Region",
    aggfunc = "sum"
)
pivot_data.plot(
    kind='bar',
    stacked=True,
    figsize=(10,6),
    color= ['pink', 'lightgreen', 'lightblue', 'purple']
)
plt.title('Category-wise Sales by Region')
plt.xlabel('Category')
plt.ylabel('Sales')
plt.savefig('Category-wise Sales by Region.png')
plt.xticks(rotation=0)
plt.show()

#Correlation Heatmap (Matplotlib only)
corr_data = supermarket[['Sales', 'Quantity', 'Profit', 'Discount']]
corr_matrix = corr_data.corr()
plt.figure(figsize=(6,5))
plt.imshow(corr_matrix)
plt.colorbar()
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.title('Correlation Heatmap')
plt.savefig('correlation_heatmap.png')
plt.show()

#Show the percentage contribution of each category to total sales using a pie chart.
category_sales = supermarket.groupby("Sub-Category")["Sales"].sum()
explode = [0.15 if i == category_sales.max() else 0 for i in category_sales]
plt.figure(figsize = (9,10))
plt.pie(
    category_sales,
    labels=category_sales.index,
    explode=explode,
    autopct='%1.1f%%',
    shadow=True,
    startangle=90,
    rotatelabels=True,
)
plt.title("Category-wise Sales Contribution")
plt.savefig('Category-wise Sales Contribution.png')
plt.show()