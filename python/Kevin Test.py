import pandas as pd
import numpy as np
import scipy.stats as stats
import statistics
import math

filename = "SampleDataset.csv"
dataset = pd.read_csv(filename, index_col=0, header=0)
attributes = dataset.columns.to_list()


case = dataset.loc['47f6c62a2855826e6dd986bd',:]
#case = dataset.loc['bac5ea84d6aad3153db5452c',:]

#print(case)
#print(len(dataset.columns.to_list()))
#print(statistics.NormalDist(mu=72, sigma=.5).zscore(73.06))
mean = dataset.mean()
std = dataset.std(axis = 0)

zscore_list = []
for i in attributes:
    try:
        zscores = statistics.NormalDist(mu=mean[i], sigma=std[i]).zscore(case[i])
    except:
        zscores = 0
    zscore_list.append(zscores)
sum_zscore = sum(zscore_list)
percentile_zscore = statistics.NormalDist(mu=0, sigma=math.sqrt(len(attributes))).zscore(sum_zscore)
final_score = statistics.NormalDist().cdf(percentile_zscore)
print(final_score*10)

#print(mean.index.to_list())
#x = stats.zscore(dataset, axis=0)
#print(x)
#[print(i) for i in mean]
