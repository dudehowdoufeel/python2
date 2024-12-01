import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(r"C:\Users\ASUS\Desktop\python2\endka\sales_data_sample.csv", encoding="ISO-8859-1")

#data cleaning

#convert 'ORDERDATE' to datetime format for easier time-based analysis
df["ORDERDATE"]=pd.to_datetime(df["ORDERDATE"], errors="coerce")

#check for duplicate rows
duplicates=df.duplicated().sum()
if duplicates>0:
    print(f"found {duplicates} duplicate rows, dropping them")
    df=df.drop_duplicates()  #drop duplicate rows if exists

#drop rows with missing values in important columns(sales,quantityordered,priceeach)
df.dropna(subset=['SALES', 'QUANTITYORDERED', 'PRICEEACH'], inplace=True)

#ensure that the necessary columns are of the correct data type
df["QUANTITYORDERED"]=df["QUANTITYORDERED"].astype(int)  #quantity should be an integer
df["SALES"]=df["SALES"].astype(float)  #sales should be a float
df["PRICEEACH"]=df["PRICEEACH"].astype(float)  #price per product should be a float

#handle outliers: use IQR (Interquartile Range) to detect and remove extreme outliers
Q1=df[['SALES', 'QUANTITYORDERED']].quantile(0.25)  #1st quartile
Q3=df[['SALES', 'QUANTITYORDERED']].quantile(0.75)  #3rd quartile
IQR=Q3-Q1  #Interquartile range

#filter out the outliers by applying the IQR rule
df=df[~((df[['SALES', 'QUANTITYORDERED']] < (Q1-1.5*IQR)) | (df[['SALES', 'QUANTITYORDERED']] > (Q3+1.5*IQR))).any(axis=1)]

#DATA ANALYSIS
#ddentify the product category that generated the highest revenue
cat_revenue=df.groupby("PRODUCTLINE")["SALES"].sum().reset_index()

highest_rev_cat=cat_revenue.loc[cat_revenue["SALES"].idxmax()]
print(f"highest revenue product category:{highest_rev_cat['PRODUCTLINE']} with revenue of ${highest_rev_cat['SALES']:,.2f}")

#find the top 5 products with the most units sold
top=df.groupby('PRODUCTCODE')['QUANTITYORDERED'].sum().reset_index()

#sort by quantity ordered in descending order and get top 5 products
top=top.sort_values(by='QUANTITYORDERED', ascending=False).head(5)

#add the product names from PRODUCTLINE to the top 5 products
top_wn=pd.merge(top, df[['PRODUCTCODE', 'PRODUCTLINE']], on='PRODUCTCODE', how='left')

#drop duplicates to get unique top 5 products
top_wn=top_wn.drop_duplicates(subset='PRODUCTCODE')

#final output of top 5 products
top_wn=top_wn[['PRODUCTCODE', 'PRODUCTLINE', 'QUANTITYORDERED']]
print("\ntop 5 products with the most units sold:")
print(top_wn)

#revenue trends over months
df['MONTH']=df['ORDERDATE'].dt.to_period('M')
monthly_revenue=df.groupby('MONTH')['SALES'].sum().reset_index()

#graphik
plt.figure(figsize=(10, 6))
plt.plot(monthly_revenue['MONTH'].astype(str), monthly_revenue['SALES'], marker='o', color='b')
plt.title('monthly revenue trends')
plt.xlabel('month')
plt.ylabel('revenue, $')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#revenue distribution across regions

#check for consistency in country names (cleaning up any extra spaces or inconsistent capitalization)
df['COUNTRY']=df['COUNTRY'].str.strip().str.title()

#group by country and calculate total sales for each region
region_revenue=df.groupby('COUNTRY')['SALES'].sum().reset_index()

#sorting regions by revenue in descending order for better visualization
region_revenue=region_revenue.sort_values(by='SALES', ascending=False)

#graphik
plt.figure(figsize=(8, 8))
plt.pie(region_revenue['SALES'], labels=region_revenue['COUNTRY'], autopct='%1.1f%%', startangle=90)
plt.title('revenue distribution by region')
plt.axis('equal')  #equal aspect ratio ensures that the pie is drawn as a circle.
plt.show()

#analyze the average product price in each category
avg_price_by_category=df.groupby('PRODUCTLINE')['PRICEEACH'].mean().reset_index()

print("\naverage price of products by category:")
print(avg_price_by_category)

#sales distribution across product lines (extra analysis)
product_line_sales=df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()

# graphik
plt.figure(figsize=(8, 8))
plt.pie(product_line_sales['SALES'], labels=product_line_sales['PRODUCTLINE'], autopct='%1.1f%%', startangle=90)
plt.title('sales distribution by product line')
plt.axis('equal')
plt.show()
