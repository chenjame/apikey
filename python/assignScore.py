import pandas as pd
import numpy as np
import scipy.stats as stats
import statistics
import math

#Calling the dataset to get a score
'''
def assignScore(filename, case):
    #filename = "SampleDataset.csv"
    dataset = pd.read_csv(filename, index_col=0, header=0)
    dataset - dataset.fillna(0)
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
'''
# Calling weights to get score
def assignScore(filename, case):
    dataset = pd.read_csv(filename, index_col=0, header=0)
    dataset - dataset.fillna(0)
    attributes = dataset.columns.to_list()
    
    mean = dataset.loc["mean",:]
    std = dataset.loc["std",:]
    weights = dataset.loc["weight",:].to_list()

    zscore_list = []
    '''
    if case["Number of Parts"] == 0: #,case["Number of Parts Features"] == 0]):
        finalscore = 0
        return finalscore
    '''
    for i in attributes:
        try:
            zscores = statistics.NormalDist(mu=mean[i], sigma=std[i]).zscore(case[i])
        except:
            zscores = 0
        zscore_list.append(zscores)
    
    sum_zscore = np.dot(zscore_list, weights)
    
    percentile_zscore = statistics.NormalDist(mu=0, sigma=math.sqrt(len(attributes))).zscore(sum_zscore)
    finalscore = statistics.NormalDist().cdf(percentile_zscore)
    finalscore = round(finalscore,3)
    print(finalscore*10)
    return finalscore*10
