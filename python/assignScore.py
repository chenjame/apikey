import pandas as pd
import numpy as np
import scipy.stats as stats
import statistics
import math

def assignScore(filename, case):
    #filename = "SampleDataset.csv"
    dataset = pd.read_csv(filename, index_col=0, header=0)
    attributes = dataset.columns.to_list()
    #print(len(attributes))

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
    finalscore = statistics.NormalDist().cdf(percentile_zscore)
    finalscore = round(finalscore,3)
    print(finalscore*10)
    return finalscore*10

