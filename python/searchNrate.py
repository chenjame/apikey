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

def get_mass_properties(did, did_list):

    return noMass

##Ask for user input:
##will have to edit this out later to only contain user input "did" and "keyword" and computer does rating
##userBase will be set to public and searchRange will always be a set value as well
#userdid = input("Enter Part or Assembly did to Rate: ")
#userInput = input("Enter Keyword for this Part: ")
userInput=input("Enter Keyword Search: ")
userBase=int(input("Enter Domain Type (0, 1, 2, 3, 4)  4 for public, 0 for my docs: "))
searchRange = int(input("Enter Number of Searches: ")) 

#idList will contain all did, wid, and eid saved to the did_list.json
idList = search_onshape_query(userInput, userBase, searchRange)

print("\n\n")

did = list(idList.keys())[0]
print(did)
#print("Number of elements in this document: " + str(element_qty_rating(did, x)))
#print("Number of workspaces in this document: " + str(workspaces_qty_rating(did, x)))
#print("Element Breakdown: ")
print(element_breakdown(did, idList))
c = element_breakdown(did, idList)
#print(c["onshape/partstudio"])

# mass properties test
testmass = get_massproperties