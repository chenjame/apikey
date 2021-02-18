import json
import sys
from onshapepy.client import Client
import pandas as pd

with open('did_list.json') as f:
  infile = json.load(f)

stacks = {
    'cad': 'https://cad.onshape.com'
}

c = Client(stack=stacks['cad'], logging=True)

#items = infile["items"][0]
#print("isEnterpriseOwned" in items)
#print(items["id"])
#feature_num = len(infile["features"])

#print("Number of features is: " + str(feature_num))

##did = list(infile.keys())[0]
##print("did:" + did)
#print("list of keys: " + list(infile.keys()))
#print(infile["bac5ea84d6aad3153db5452c"]["wid"])



'''
feature_types = []
feature_count = len(infile["features"])


for i in range(feature_count):
  feature_types.append(infile["features"][i]["message"]["featureType"])

print("List of features:", feature_types)

'''


did = "bac5ea84d6aad3153db5452c"
#print(len(infile[did]["wid"]))

def feature_tree_count(did, id_list):
    # looking at one specific DID
    feature_count = 0
    feature_types = []

    wid_list = id_list[did]["wid"]
    eid_list = id_list[did]["eid"]
    for wid in range(len(wid_list)):
            for eid in range(len(eid_list)):
                fcount, ftypes = c.get_feature_list(did, id_list[did]["wid"][wid], id_list[did]["eid"][eid])
                feature_count = feature_count + fcount
                feature_types.extend(ftypes)
    
    return feature_count, feature_types

feature_count, feature_types = feature_tree_count(did, infile)
print("Feature count:", feature_count)
print("Feature types:", feature_types)
type_tally = pd.Index(feature_types)
print(type_tally.value_counts())






"""
did = "3f52b4a599ab60d07b138028"
wid = "515cdd29bd85642ac09a651f"
eid = "afcbf0ae1cc776b1b1f6b1b9"

count, testlist = c.get_feature_list(did, wid, eid)

print(count)
print(testlist)
"""


#print(len(infile))