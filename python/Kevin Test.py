import pandas as pd
import numpy as np
import scipy.stats as stats

filename = "SampleDataset.csv"
dataset = pd.read_csv(filename, index_col=0, header=0)
mean = dataset.mean()
std = dataset.std(axis = 0)
x = stats.zscore(dataset, axis=0)
[print(sum(i)) for i in x]
