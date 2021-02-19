import json
import sys
from onshapepy.client import Client
import pandas as pd

with open('RES_OUTPUT.json') as f:
  infile = json.load(f)



"""
stacks = {
    'cad': 'https://cad.onshape.com'
}

c = Client(stack=stacks['cad'], logging=True)
"""


res = infile
asy_feature_types = []


feature_count = len(res["features"])

#print('\n["features"][i]["message"]["parameters"][0]["message"]["value"]')

# add each new feature type found to the list of feature types
for i in range(feature_count):
  try:
    if res["features"][i]["typeName"] == "BTExplosion":
      asy_feature_types.append("EXPLODED_VIEW")
    elif res["features"][i]["message"]["parameters"][0]["message"]["value"] == "CIRCULAR":
      asy_feature_types.append("CIRCULAR_PATTERN")
    elif res["features"][i]["message"]["parameters"][0]["message"]["value"] == "ON_ENTITY":
      asy_feature_types.append("MATE_CONNECTOR")
    elif res["features"][i]["message"]["parameters"][0]["message"]["value"] == "LINEAR":
      if res["features"][i]["message"]["parameters"][0]["message"]["enumName"] == "Pattern type":
        asy_feature_types.append("LINEAR_PATTERN")
      else:
        asy_feature_types.append("LINEAR_MATE")
    else:
      asy_feature_types.append(res["features"][i]["message"]["parameters"][0]["message"]["value"])
  except KeyError:
    #print("key error")
    try:
      if res["features"][i]["message"]["featureType"] == "geometryMate":
        asy_feature_types.append("TANGENT")
      elif res["features"][i]["message"]["featureType"] == "mateGroup":
        asy_feature_types.append("MATE_GROUP")
    except:
      print("\n\n\n\n\nA wild Assembly Feature Appeared\n\n\n\n\n\n\n")
      asy_feature_types.append("UNACCOUNTED_ASY_FEATURE")
  except IndexError:
    print("\n\n\n\n\nA wild Assembly Feature Appeared\n\n\n\n\n\n\n")
    asy_feature_types.append("UNACCOUNTED_ASY_FEATURE")
    


#print("\n")
print("Features: ", feature_count)
print("Features: ", asy_feature_types)



##################################################################


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
"""

did = "47b0488b3684bd60799b73a2"
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

#put document ID values in json file called did_list.json
#with open("std_feature_list.json", "w") as json_file:
 # json.dump(feature_types, json_file)



type_tally = pd.Index(feature_types)
print(type_tally.value_counts())



"""


"""
did = "3f52b4a599ab60d07b138028"
wid = "515cdd29bd85642ac09a651f"
eid = "afcbf0ae1cc776b1b1f6b1b9"

count, testlist = c.get_feature_list(did, wid, eid)

print(count)
print(testlist)
"""