from __future__ import print_function

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
userBase=int(input("Enter Domain Type (0, 1, 2, 3, 4): "))
#userBase = int(userBase)
userDiction= {'q': userInput,'filter': userBase}

# get document details
searchResults = c.list_documents(userDiction)



