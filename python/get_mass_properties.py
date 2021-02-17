from __future__ import print_function
import json
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
    # binary true/false for if any part does not have a mass then score lower
    # need to know which element ids are partstudios and which are assemblies

    for i in range(len(id_list[did]["wid"])):
        for j in range(len(id_list[did]["eid"])):
            getmassprop = c.get_massproperties(did, str(id_list[did]["wid"][i]), str(id_list[did]["eid"][j]))

            if getmassprop["bodies"]["-all-"]["massMissingCount"] != 0:
                hasMass = False
            else:
                hasMass = True

    return hasMass

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

##Ask for user input:
##will have to edit this out later to only contain user input "did" and "keyword" and computer does rating
##userBase will be set to public and searchRange will always be a set value as well
#userdid = input("Enter Part or Assembly did to Rate (no did given, will default your did): ")
#userInput = input("Enter Keyword for this Part: ")
userInput=input("Enter Keyword Search: ")
userBase=int(input("Enter Domain Type (0 self, 1, 2, 3, 4 public)  4 for public, 0 for my docs: "))
searchRange = int(input("Enter Number of Searches: ")) 

#idList will contain all did, wid, and eid saved to the did_list.json
idList = search_onshape_query(userInput, userBase, searchRange)

print("\n\n")

did = list(idList.keys())[0]
print(did)
#print("Number of elements in this document: " + str(element_qty_rating(did, idList)))
#print("Number of workspaces in this document: " + str(workspaces_qty_rating(did, idList)))
#print("Element Breakdown: ")
#print(element_breakdown(did, idList))
#c = element_breakdown(did, idList)
#print(c["onshape/partstudio"])

# mass properties test
hasMass = get_mass_properties(did, idList)
print(hasMass)
