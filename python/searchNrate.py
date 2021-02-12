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

userInput=input("Enter Keyword Search: ")
userBase=int(input("Enter Domain Type (0, 1, 2, 3, 4)  4 for public, 0 for my docs: "))
searchRange = int(input("Enter Number of Searches: ")) 
items = {}

'''
Proposed master dictionary structure, to be refined
{
    "did1" : {"wid": [list of wids], "EID":[list of EIDS]}

}
'''

## Build FOR loop here for searching
for search_offset in range(searchRange):
    userDiction= {'q': userInput,'filter': userBase, "limit" : searchRange, "offset": search_offset}
    
    # get document details
    search_did = c.list_documents(userDiction)
    
    search_ws = c.get_workspaces(search_did)

    search_eid = c.get_elementid(search_did, search_ws)
    
    items[search_offset] = search_did

#put document ID values in json file called did_list.json
with open("did_list.json", "w") as json_file:
    json.dump(items, json_file)


#wid
for search_offset in range(searchRange):
    search_ws = c.get_workspaces(items[search_offset])


with open("ws_list.json", "w") as json_file:
    json.dump(items, json_file)

#eid
for search_offset in range(searchRange):
    search_eid = c.get_elementid(items[search_offset])

with open("eid_list.json", "w") as json_file:
    json.dump(items, json_file)
