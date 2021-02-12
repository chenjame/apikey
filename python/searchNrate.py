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
userBase=int(input("Enter Domain Type (0, 1, 2, 3, 4): 4 for public, 0 for my docs "))
#userBase = int(userBase)
items = {}

## Build FOR loop here for searching
for search_offset in range(5):
    userDiction= {'q': userInput,'filter': userBase, "limit" : 1, "offset": search_offset}
    
    # get document details
    searchResults = c.list_documents(userDiction)

    with open('RES_OUTPUT.json') as f:
        infile = json.load(f)

    did_index = search_offset
    items[did_index] = infile["items"][0]["id"]


with open("did_list.json", "w") as json_file:
    json.dump(items, json_file)



