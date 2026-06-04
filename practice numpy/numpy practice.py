import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
supermarket = pd.read_csv('superstore_data.csv', encoding='latin1')

#Category-wise sales split by region.
pivot_data = supermarket.pivot_table(
    index = "Category",
    values = "Sales",
    columns = "Region",
    aggfunc = "sum"
)
pivot_data.plot(
    kind='bar',
    stacked='True',
    figsize=(10,6),
    color= ['pink', 'lightgreen', 'lightblue', 'purple']
)
plt.title('Category-wise Sales by Region')
plt.xlabel('Category')
plt.ylabel('Sales')
plt.savefig('Category-wise Sales by Region.png')
plt.xticks(rotation=0)
plt.show()
