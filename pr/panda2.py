import pandas as pd

data = {
    "date": [
        "2024-01-01",
        "2024-01-02",
        "2024-01-03",
        "2024-01-04", 
        "2024-01-05",
        "2024-01-06",
        "2024-01-07",
        "2024-01-08", 
        "2024-01-09",
        "2024-01-10"
    ],
    "sales": [200, 150, 300, 400, 500, 450, 600, 350, 300, 250]
}
a=pd.DataFrame(data)
tot=a["sales"].sum()
ave=a["sales"].mean()

max=a.loc[a["sales"].idxmax()]
min=a.loc[a["sales"].idxmin()]

print(a)
print(f"total sales {tot}")
print(f"ave sales per day {ave}")
print(f"day max sales {max['date']} {max['sales']}")
print(f"day min sales {min['date']} {min['sales']}")
