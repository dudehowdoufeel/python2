import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie", "David", "Emma", "Miya", "Chara", "Inkar", "Zhaxs", "Kesha", "Toma", "Ilyas"],
    "age": [25, 32, 30, 29, 28, 18, 18, 18, 18, 19, 18, 20],
    "salary": [50000, 60000, 45000, 70000, 65000, 80000, 75000, 60000, 80000, 70000, 50000, 100000],
    "department": ["HR", "Finance", "IT", "Marketing", "Finance", "IT", "Finance", "Finance", "IT", "Marketing", "HR", "IT"]
}
a=pd.DataFrame(data)
grouped=a.groupby("department")
ave=grouped["salary"].mean()
total=grouped["name"].count()

print("ave salary by dep")
print(ave.to_string())
print(total.to_string())
