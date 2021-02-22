import pandas as pd
import numpy as np
import scipy.stats as stats
import statistics
import math

def concatFiles(all_files, final_filename):
    # This function takes in a list of filenames and stitches them together.
    # The new dataset is then exported to a CSV under the final_filename given.
    file_list = []
    for filename in all_files:
        data = pd.read_csv(filename, index_col=0, header=0)
        #print(data.shape)
        file_list.append(data)

    dataset = pd.concat(file_list, axis=0, ignore_index=False)
    dataset = dataset.fillna(0)
    dataset.to_csv(final_filename, header = True)
    print("Your files have been stitched together!")
    return dataset
'''
all_files = ["completeDataset.csv", "newDataset.csv"]
final_filename = "completeDataset.csv"
full_dataset = concatFiles(all_files, final_filename)
'''

def getZScore(filename):
    dataset = pd.read_csv(filename, index_col=0, header=0)
    dataset - dataset.fillna(0)

    did_values = dataset.index.to_list()
    attributes_names = dataset.columns.to_list()
    
    #print(dataset.shape)
    #print(len(did_values), len(attributes_names))
    
    mean = dataset.mean()
    std = dataset.std(axis = 0)

    zscore_list = []

    for did in did_values:
        case = dataset.loc[did,:]
        case_scores = []
        for attribute in attributes_names:
            try:
                zscores = statistics.NormalDist(mu=mean[attribute], sigma=std[attribute]).zscore(case[attribute])
            except:
                zscores = 0
            case_scores.append(zscores)
        
        sum_zscore = sum(case_scores)
        percentile_zscore = statistics.NormalDist(mu=0, sigma=math.sqrt(len(attributes_names))).zscore(sum_zscore)
        finalscore = statistics.NormalDist().cdf(percentile_zscore)
        finalscore = round(finalscore,3) *10
        zscore_list.append(finalscore)
    return zscore_list

'''
filename = "completeDataset.csv"
did_zscores = getZScore(filename)
#print(statistics.mean(did_zscores))

masterdataset = pd.read_csv(filename, index_col=0, header=0)
print(masterdataset.shape)
masterdataset["score"] = did_zscores
masterdataset.to_csv("completeDatasetScored.csv",header = True)
#print( sum([1 for i in did_zscores if i <4 ]))
'''
df = pd.read_csv("completeDataset.csv", index_col = 0, header = 0)
print(df.columns.to_list())
'''
#mean = df.mean()
#std = df.std(axis = 0)

dataset = pd.DataFrame()
dataset["mean"] = mean
dataset["std"] = std
dataset =dataset.T
dataset.to_csv("weights.csv", header = True)
'''
