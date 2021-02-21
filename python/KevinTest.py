import pandas as pd

df = pd.read_csv("KevinDataset.csv", index_col=0, header=0)
print(df.shape)