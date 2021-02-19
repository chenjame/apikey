from __future__ import print_function
import json
import csv
import pandas as pd
'''
enVision 2021 PTC Hackathon

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

'''
Proposed master dictionary structure
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
    #with open("did_list.json", "w") as json_file:
    #    json.dump(items, json_file)

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
    
    #assemblyList= [id_list[did]["eid"][j] for j, val in enumerate(id_list[did]["element types"]) if val == "onshape/assembly"]

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
    # create list of eids with just PARTSTUDIOS 
    eid_list = [id_list[did]["eid"][j] for j, val in enumerate(id_list[did]["element types"]) if val == "onshape/partstudio"]
    # eid_list = id_list[did]["eid"] # the original one just pulled all the EIDs

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
    feature_types = type_tally.value_counts()

    return feature_count, feature_types

def asy_feature_tree_count(did, id_list):
    # looking at one specific DID, tries all the WID & EID combos within the DID and gets a master count of how many 
    # features and types of features there are 
    asy_feature_count = 0
    asy_feature_types = []

    # looks inside the did_list.json file and identifies the list of WID and EIDs associated with this particular DID
    wid_list = id_list[did]["wid"]
    # create list of eids with just Asemblies EIDs 
    eid_list = [id_list[did]["eid"][j] for j, val in enumerate(id_list[did]["element types"]) if val == "onshape/assembly"]

    #iterate through the WIDs
    for wid in range(len(wid_list)):
            # then iterating through the EIDs for a given WID
            for eid in range(len(eid_list)):
                # calls the get_asy_feature_list function, gets a count and list of types as return. 
                # If call fails, 0 as count and a blank list gets returned
                fcount, ftypes = c.get_asy_feature_list(did, id_list[did]["wid"][wid], id_list[did]["eid"][eid])
                # adds the count to the running tally
                asy_feature_count = asy_feature_count + fcount
                # appends the new list of types to the existing list
                asy_feature_types.extend(ftypes)
    
    # tallying up all the feature types in this DID
    type_tally = pd.Index(asy_feature_types)
    asy_feature_types = type_tally.value_counts()

    return asy_feature_count, asy_feature_types

def count_versions (did):
    #call function to find out how many versions there are of the did
    numVersions = c.get_versions(did)

    return numVersions

def did_from_url(url):
    startIndex = url.find("/documents/") + 11 #3 #find where the start of /d/ for did + 3 indecies bc of "/" + "d" + "/"
    try:
        endIndex = url.find("/w")
    
    except:
        endIndex = url.find("/v")
    did = "" #initialize did as a str

    #build did from url chr by chr
    for i in range (startIndex, endIndex):
        did += url[i]
    return did

def userWIDEID(did):
    items = {}
    # create a dictionary that will store the lists of wids and eids
    did_components = {}
    search_ws = c.get_workspaces(did)
    did_components["wid"] = search_ws

    search_eid, element_type = c.element_list(did, search_ws)
    did_components["eid"] = search_eid
    ##adding the element types
    did_components["element types"] = element_type

    items[did] = did_components

    #put document ID values in json file called did_list.json
    #with open("did_list.json", "w") as json_file:
    #    json.dump(items, json_file)

    return items

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
    case = case.append(feature_types)

    asy_feature_count, asy_feature_types = asy_feature_tree_count(did, did_list)
    case["Number of Assembly Features"] = asy_feature_count
    case = case.append(asy_feature_types)

    case = case.rename(did)
    return case

attribute_list = ['Number of Features', 'Number of Parts', 'Number of Total Elements', 'Number of Versions', 'Number of Workspaces', 'Parts Missing Mass', 'application/step', 'application/stl', 'onshape-app/com.onshape.api-explorer', 'onshape-app/drawing', 'onshape-app/materials', 'onshape/assembly', 'onshape/billofmaterials', 'onshape/featurestudio', 'onshape/partstudio', 'newSketch', 'extrude', 'revolve', 'sweep', 'cPlane', 'loft', 'thicken', 'enclose', 'fillet', 'chamfer', 'draft', 'rib', 'shell', 'hole', 'linearPattern', 'circularPattern', 'curvePattern', 'mirror', 'booleanBodies', 'splitPart', 'transform', 'wrap', 'deleteBodies', 'modifyFillet', 'deleteFace', 'moveFace', 'replaceFace', 'offsetSurface', 'fill', 'extendSurface', 'helix', 'fitSpline', 'projectCurves', 'bridgingCurve', 'compositeCurve', 'mateConnector', 'importDerived', 'assignVariable', 'compositePart', 'sheetMetalStart', 'sheetMetalFlange', 'sheetMetalHem', 'sheetMetalTab', 'sheetMetalMakeJoint', 'sheetMetalCorner', 'sheetMetalBendRelief', 'sheetMetalJoint', 'sheetMetalEnd', 'sheetMetalEndMATE_CONNECTOR', 'FASTENED', 'REVOLUTE', 'SLIDER', 'PLANAR', 'CYLINDRICAL', 'PIN_SLOT', 'BALL', 'PARALLEL', 'TANGENT', 'MATE_GROUP', 'GEAR', 'RACK_AND_PINION', 'SCREW', 'LINEAR_MATE', 'LINEAR_PATTERN', 'CIRCULAR_PATTERN', 'Number of Assembly Features']

def createTestSet(did_list):
    # this function takes in a list of IDs and then constructs a dataset 
    # that is n by m, in which n is the number of DIDs and m is number of variables.
    data = pd.DataFrame(columns = attribute_list)
    for did in list(did_list.keys()):
        case = createAttributes(did, did_list)
        data = data.append(case)
    data = data.fillna(0)
    return data

def updateDataset(filename, new_dataset):
    list_dataset = []
    og_dataset = pd.read_csv(filename,index_col=0, header=0)
    
    list_dataset.append(og_dataset)
    list_dataset.append(new_dataset)

    master_dataset = pd.concat(list_dataset, axis=0)
    
    master_dataset.to_csv(filename, header=True)
    print("Your dataset has been updated!")

################################## Uncomment this Area to Call QUERY##################################
'''
userInput=input("Enter Keyword Search: ")
userBase=int(input("Enter Domain Type (0 self, 1, 2, 3, 4 public)  4 for public, 0 for my docs: "))
searchRange = int(input("Enter Number of Searches: ")) 

##idList will contain all did, wid, and eid saved to the did_list.json
idList = search_onshape_query(userInput, userBase, searchRange)
'''
######################################################################################################


#######################################Create Dataset#################################################
#createAttributes(did, did_list)
##in case someone deletes sampledataset
#firstdataset = pd.DataFrame(columns = attribute_list)
#firstdataset.to_csv(filename, header= True)

'''
filename = "SampleDataset.csv"
new_dataset = createTestSet(idList)
updateDataset(filename, new_dataset)
'''
######################################################################################################