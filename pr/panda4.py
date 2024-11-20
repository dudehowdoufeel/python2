import pandas as pd
import numpy as np

data = {
    "product": ["apple","banana","orange","grapes","mango"],
    "price": [100, 80, np.nan, 120, np.nan],
    "stock": [10, np.nan, 5, 7, np.nan]
}
a=pd.DataFrame(data)

ave=a["price"].mean()
a["price"].fillna(ave, inplace=True)
a["stock"].fillna(0, inplace=True)
print(a)
