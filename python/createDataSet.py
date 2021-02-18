from __future__ import print_function
import json
import csv
import pandas as pd
'''
app
===

#Copied basic structure from app.py
'''

#from apikey.client import Client
from onshapepy.client import Client

# stacks to choose from
stacks = {
    'cad': 'https://cad.onshape.com'
}

# create instance of the onshape client; change key to test on another stack
c = Client(stack=stacks['cad'], logging=True)

# make a new document and grab the document ID and workspace ID
#new_doc = c.new_document(public=True).json()
#did = new_doc['id']
#wid = new_doc['defaultWorkspace']['id']



'''
Proposed master dictionary structure, to be refined
{
    "did1" : {"wid": [list of wids], "EID":[list of EIDS]}

}
'''

'''
DEFINITIONS:

did = document ID / your entire file containing your workspaces, elements (parts, API, assemblies, drawings, imports, etc.)
wid = workspace ID / your workspace (main, branches, etc) that show up in your branch history list (open circle)
eid = element ID / your tabs in your did and wid (parts, API, assemblies, drawings, imports, etc.)
version = different saves of the workspace at a specified instance with its corresponding elements

'''

def search_onshape_query(userInput, userBase, searchRange): 

    items = {}
    
    for search_offset in range(searchRange):
        userDiction= {'q': userInput,'filter': userBase, "limit" : searchRange, "offset": search_offset}
        
        # get document details
        search_did = c.list_documents(userDiction)
        
        # create a dictionary that will store the lists of wids and eids
        did_components = {}
        search_ws = c.get_workspaces(search_did)
        did_components["wid"] = search_ws

        search_eid, element_type = c.element_list(search_did, search_ws)
        did_components["eid"] = search_eid
        ##adding the element types
        did_components["element types"] = element_type

        
        items[search_did] = did_components

    #put document ID values in json file called did_list.json
    with open("did_list.json", "w") as json_file:
        json.dump(items, json_file)

    return items


def element_qty_rating(did, did_list):

    element_qty = len(did_list[did]["eid"])

    return element_qty

def workspaces_qty_rating(did, did_list):
    
    workspaces_qty = len(did_list[did]["wid"])

    return workspaces_qty

def element_breakdown(did, did_list):
    elements = pd.Series(did_list[did]["element types"])
    counts = elements.value_counts()
    return counts

def get_mass_properties(did, id_list):
    # initiate missing mass part count and total num parts in eid
    missingMassParts = 0
    totalNumParts = 0
    
    # create list of eids with just PARTSTUDIOS 
    partsList= [id_list[did]["eid"][j] for j, val in enumerate(id_list[did]["element types"]) if val == "onshape/partstudio"]
    
    # set widList as the list of wid for simplicity
    widList = id_list[did]["wid"]
    # count num of parts without mass/material and num of elements in eids
    for wid in widList:
        for eid in partsList:
            missingMassParts += c.get_massproperties(did, wid, eid)
            totalNumParts += c.get_parts_in_partstudio(did, wid, eid)
   
    return missingMassParts, totalNumParts # returns number of parts with missing mass in a did and num of parts in eids 

def feature_tree_count(did, id_list):
    # looking at one specific DID, tries all the WID & EID combos within the DID and gets a master count of how many 
    # features and types of features there are 
    feature_count = 0
    feature_types = []

    # looks inside the did_list.json file and identifies the list of WID and EIDs associated with this particular DID
    wid_list = id_list[did]["wid"]
    eid_list = id_list[did]["eid"]

    #iterate through the WIDs
    for wid in range(len(wid_list)):
            # then iterating through the EIDs for a given WID
            for eid in range(len(eid_list)):
                # calls the get_feature_list function, gets a count and list of types as return. 
                # If call fails, 0 as count and a blank list gets returned
                fcount, ftypes = c.get_feature_list(did, id_list[did]["wid"][wid], id_list[did]["eid"][eid])
                # adds the count to the running tally
                feature_count = feature_count + fcount
                # appends the new list of types to the existing list
                feature_types.extend(ftypes)
    
    # tallying up all the feature types in this DID
    type_tally = pd.Index(feature_types)
    print(type_tally.value_counts())

    return feature_count, feature_types

def count_versions (did):
    #call function to find out how many versions there are of the did
    numVersions = c.get_versions(did)

    return numVersions

def did_from_url (url):
    startIndex = url.find("/d/") + 3 #find where the start of /d/ for did + 3 indecies bc of "/" + "d" + "/"
    endIndex = url.find("/w/")
    did = "" #initialize did as a str

    #build did from url chr by chr
    for i in range (startIndex, endIndex):
        did += url[i]
    return did

def createAttributes(did, did_list):
    # this function takes in a did and its did list to create an case to add to dataset 
    case = pd.Series()
    case = case.append(element_breakdown(did, did_list))
    case["Number of Total Elements"] = element_qty_rating(did, did_list)
    case["Number of Workspaces"] = workspaces_qty_rating(did, did_list)
    case["Number of Versions"] = count_versions(did)
    
    missingMassParts, totalNumParts = get_mass_properties(did, did_list)
    case["Parts Missing Mass"] = missingMassParts
    case["Number of Parts"] =  totalNumParts

    feature_count, feature_types = feature_tree_count(did, did_list)
    case["Number of Features"] = feature_count
    case = case.rename(did)
    return case


def createTestSet(did_list):
    # this function takes in a list of IDs and then constructs a dataset 
    # that is n by m, in which n is the number of DIDs and m is number of variables.
    data = pd.DataFrame()
    for did in list(did_list.keys()):
        case = createAttributes(did, did_list)
        data = data.append(case)
    data = data.fillna(0)
    return data



################################## Uncomment this Area to Call QUERY##################################
userInput=input("Enter Keyword Search: ")
userBase=int(input("Enter Domain Type (0 self, 1, 2, 3, 4 public)  4 for public, 0 for my docs: "))
searchRange = int(input("Enter Number of Searches: ")) 

##idList will contain all did, wid, and eid saved to the did_list.json
idList = search_onshape_query(userInput, userBase, searchRange)
######################################################################################################


print("\n\n")

#######################################Create Dataset#################################################
#did = "bac5ea84d6aad3153db5452c" 
#idList = {"bac5ea84d6aad3153db5452c": {"wid": ["24321161ec81bce2b1df6cda", "b924da502c3f8bf01ed95c05"], "eid": ["f20c6cb4fa20fa25f30734ff", "07fc595ebdaf9eb383e97276", "dc93dd30f1d4c0251d76ab3e", "880daf10f99c227b26189f6c", "07ee6adf4c5269d34f572d3a", "7a0f8b1e3cf03cf20c957922", "5081b4aa63de5997415b72de", "013bab8b899efd6b32701bb2", "789cd84e63d6f8c534c072ff", "d3591b03919ce594327c6de5", "b82ff955383aba26a6315a1e"], "element types": ["onshape/partstudio", "application/stl", "onshape-app/com.onshape.api-explorer", "onshape/partstudio", "onshape/assembly", "onshape-app/materials", "onshape/featurestudio", "onshape-app/drawing", "onshape/billofmaterials", "application/step", "onshape/partstudio"]}}
#createAttributes(did, did_list)
dataset = createTestSet(idList)
dataset.to_csv("SampleDataset.csv",header=True)
######################################################################################################


#did = list(idList.keys())[0]
#print(did)
#print("Number of elements in this document: " + str(element_qty_rating(did, idList)))
#print("Number of workspaces in this document: " + str(workspaces_qty_rating(did, idList)))
#print("Element Breakdown: ")
#print(element_breakdown(did, idList))
#c = element_breakdown(did, idList)
#print(c["onshape/partstudio"])

# mass properties test
#missingMassCount, numParts = get_mass_properties(did, idList)
#print(missingMassCount)
#print(numParts)

# version count test
# print(count_versions(did))

# did from url test
#url = "https://cad.onshape.com/d/bac5ea84d6aad3153db5452c/w/24321161ec81bce2b1df6cda/e/f20c6cb4fa20fa25f30734ff/"
#print(did_from_url(url))