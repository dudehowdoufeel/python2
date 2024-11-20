import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "age": [25, 32, 30, 29, 28],
    "salary": [50000, 60000, 45000, 70000, 65000],
    "department": ["HR", "Finance", "IT", "Marketing", "Finance"]
}
a = pd.DataFrame(data)

a["bonus"] = a["salary"] * 0.10

new_a = a[a["salary"] > 50000]
print(a)
print("\nfiltered")
print(new_a)
