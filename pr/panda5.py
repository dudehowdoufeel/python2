import pandas as pd
import matplotlib.pyplot as plt
data = {
    "name": ["Alice", "Bob", "Charlie", "David", "Emma", "Miya", "Chara", "Inkar", "Zhaxs", "Kesha", "Toma", "Ilyas"],
    "age": [25, 32, 30, 29, 28, 18, 18, 18, 18, 19, 18, 20],
    "salary": [50000, 60000, 45000, 70000, 65000, 80000, 75000, 60000, 80000, 70000, 50000, 100000],
    "department": ["HR", "Finance", "IT", "Marketing", "Finance", "IT", "Finance", "Finance", "IT", "Marketing", "HR", "IT"]
}
a = pd.DataFrame(data)
grouped = a.groupby("department")
ave = grouped["salary"].mean()
total = grouped["name"].count()

plt.figure(figsize=(8, 6))
ave.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Average Salary by Department', fontsize=16)
plt.xlabel('Department', fontsize=12)
plt.ylabel('Average Salary', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
