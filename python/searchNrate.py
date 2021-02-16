from __future__ import print_function
import json

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


def search_onshape_query(): 
    ## Build FOR loop here for searching
    userInput=input("Enter Keyword Search: ")
    userBase=int(input("Enter Domain Type (0, 1, 2, 3, 4)  4 for public, 0 for my docs: "))
    searchRange = int(input("Enter Number of Searches: ")) 
    
    
    items = {}
    
    for search_offset in range(searchRange):
        userDiction= {'q': userInput,'filter': userBase, "limit" : searchRange, "offset": search_offset}
        
        # get document details
        search_did = c.list_documents(userDiction)
        
        # create a dictionary that will store the lists of wids and eids
        did_components = {}
        search_ws = c.get_workspaces(search_did)
        did_components["wid"] = search_ws

        search_eid = c.element_list(search_did, search_ws)
        did_components["eid"] = search_eid

        
        items[search_did] = did_components

    #put document ID values in json file called did_list.json
    with open("did_list.json", "w") as json_file:
        json.dump(items, json_file)

    return items


def part_qty_rating(did, did_list):

    part_qty = len(did_list[did]["eid"])

    return part_qty

def workspaces_qty_rating(did, did_list):
    
    workspaces_qty = len(did_list[did]["wid"])

    return workspaces_qty



x = search_onshape_query()

print("\n\n")
did = list(x.keys())[0]
print("Number of parts in this document: " + str(part_qty_rating(did, x)))
print("Number of workspaces in this document: " + str(workspaces_qty_rating(did, x)))
