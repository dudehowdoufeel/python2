import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.DataFrame({
    'product': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
    'region': ['north', 'south', 'east', 'west', 'north', 'south', 'east', 'west', 'north', 'south', 'east', 'west'],
    'sales': [20000, np.nan, 27000, 31000, 35000, 40000, np.nan, 42000, 38000, 45000, 36000, 48000],
    'price': [300, 250, 320, 300, 250, 320, 300, 250, 320, 300, 250, 320],
    'date': pd.to_datetime([
        '2024-01-15', '2024-02-20', '2024-03-10', '2024-04-18', '2024-05-22', 
        '2024-06-05', '2024-07-12', '2024-08-25', '2024-09-07', '2024-10-19', 
        '2024-11-15', '2024-12-01'
    ])
})

print("missing values before cleaning:")
print(data.isnull().sum())

average_sales = np.nanmean(data['sales'])
print(f"\naverage value used to fill missing sales: {average_sales}")
data['sales'].fillna(average_sales, inplace=True)

data['revenue'] = data['sales'] * data['price']

print("\ncleaned data:")
print(data)

product_sum = data.groupby('product').agg({'sales': 'sum', 'revenue': 'sum'})
region_sum = data.groupby('region').agg({'revenue': 'sum'})
ave_revenue = data.groupby('product')['revenue'].mean()

print("\ntotal sales and revenue by product:")
print(product_sum)

print("\ntotal revenue by region:")
print(region_sum)

print("\naverage revenue by product:")
print(ave_revenue)

monthly_sales = data.groupby(data['date'].dt.month)['sales'].sum()
print("\ntotal sales by month:")
print(monthly_sales)

ax = product_sum['revenue'].plot(kind='bar', color='skyblue', figsize=(8, 6))
plt.title("total revenue by product")
plt.xlabel("product")
plt.ylabel("revenue")
plt.xticks(rotation=0)

for i, v in enumerate(product_sum['revenue']):
    ax.text(i, v + 1000, f"{int(v)}", ha='center', va='bottom')

plt.show()

region_sum['revenue'].plot(kind='pie', autopct='%1.1f%%', startangle=140, figsize=(8, 6))
plt.title("revenue share by region")
plt.ylabel("")  
plt.show()
