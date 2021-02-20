'''
client
======

Convenience functions for working with the Onshape API
'''

import sys

if sys.version_info.major < 3:
    from onshape import Onshape
else:
    from .onshape import Onshape

import mimetypes
import random
import string
import os
import pandas as pd

class Client():
    '''
    Defines methods for testing the Onshape API. Comes with several methods:

    - Create a document
    - Delete a document
    - Get a list of documents

    Attributes:
        - stack (str, default='https://cad.onshape.com'): Base URL
        - logging (bool, default=True): Turn logging on or off
    '''

    def __init__(self, stack='https://cad.onshape.com', creds='./creds.json', logging=True):
        '''
        Instantiates a new Onshape client.

        Args:
            - stack (str, default='https://cad.onshape.com'): Base URL
            - creds (str, default='./cred.json'): location of OnShape credentials (access key and secret key)
            - logging (bool, default=True): Turn logging on or off
        '''

        self._stack = stack
        self._api = Onshape(stack=stack, creds=creds, logging=logging)


    def new_document(self, name='Test Document', owner_type=0, public=False):
        '''
        Create a new document.

        Args:
            - name (str, default='Test Document'): The doc name
            - owner_type (int, default=0): 0 for user, 1 for company, 2 for team
            - public (bool, default=False): Whether or not to make doc public

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name,
            'ownerType': owner_type,
            'isPublic': public
        }

        return self._api.request('post', '/api/documents', body=payload)

    def rename_document(self, did, name):
        '''
        Renames the specified document.

        Args:
            - did (str): Document ID
            - name (str): New document name

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name
        }

        return self._api.request('post', '/api/documents/' + did, body=payload)

    def del_document(self, did):
        '''
        Delete the specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('delete', '/api/documents/' + did)

    def get_document(self, did):
        '''
        Get details for a specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/documents/' + did)

    def list_documents(self, query={}):
        '''
        Get list of documents for current user.

        Returns:
            - requests.Response: Onshape response data
        '''        
        # saves the request results into res
        res = self._api.request('get', '/api/documents', query)
        
        # convert res into a json object before indexing into it on the next line
        res = res.json()

        # extracts did from results dictionary
        did = res["items"][0]["id"]

        # returns did
        return did

    def create_assembly(self, did, wid, name='My Assembly'):
        '''
        Creates a new assembly element in the specified document / workspace.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - name (str, default='My Assembly')

        Returns:
            - requests.Response: Onshape response data
        '''

        payload = {
            'name': name
        }

        return self._api.request('post', '/api/assemblies/d/' + did + '/w/' + wid, body=payload)
    
    """
    def get_features(self, did, wid, eid):
        '''
        Gets the feature list for specified document / workspace / part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/features')
    """

    def get_partstudio_tessellatededges(self, did, wid, eid):
        '''
        Gets the tessellation of the edges of all parts in a part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/tessellatededges')

    def upload_blob(self, did, wid, filepath='./blob.json'):
        '''
        Uploads a file to a new blob element in the specified doc.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - filepath (str, default='./blob.json'): Blob element location

        Returns:
            - requests.Response: Onshape response data
        '''

        chars = string.ascii_letters + string.digits
        boundary_key = ''.join(random.choice(chars) for i in range(8))

        mimetype = mimetypes.guess_type(filepath)[0]
        encoded_filename = os.path.basename(filepath)
        file_content_length = str(os.path.getsize(filepath))
        blob = open(filepath)

        req_headers = {
            'Content-Type': 'multipart/form-data; boundary="%s"' % boundary_key
        }

        # build request body
        payload = '--' + boundary_key + '\r\nContent-Disposition: form-data; name="encodedFilename"\r\n\r\n' + encoded_filename + '\r\n'
        payload += '--' + boundary_key + '\r\nContent-Disposition: form-data; name="fileContentLength"\r\n\r\n' + file_content_length + '\r\n'
        payload += '--' + boundary_key + '\r\nContent-Disposition: form-data; name="file"; filename="' + encoded_filename + '"\r\n'
        payload += 'Content-Type: ' + mimetype + '\r\n\r\n'
        payload += blob.read()
        payload += '\r\n--' + boundary_key + '--'

        return self._api.request('post', '/api/blobelements/d/' + did + '/w/' + wid, headers=req_headers, body=payload)

    def part_studio_stl(self, did, wid, eid):
        '''
        Exports STL export from a part studio

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''

        req_headers = {
            'Accept': 'application/vnd.onshape.v1+octet-stream'
        }
        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/stl', headers=req_headers)

### extra functions added ###
    def get_bodydetails(self, did, wid, eid):
        '''
        Gets the tessellation of the edges of all parts in a part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''
        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/bodydetails')

    def get_massproperties(self, did, wid, eid):
        '''
        Collects data on part studio part mass, if no mass "hasMass" = false, if missing mass "massMissingCount" = numb missing mass parts

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''
        res = self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/massproperties')

        if res == 400:
            # if API call fails, then the WID and EID combo is no good. Return 0 as the count and the blank feature_types list
            count = 0
            return count
        else:
            res = res.json()
            try:
                count = res["bodies"]["-all-"]["massMissingCount"]
            except KeyError:
                count = 0
            return count #gives number of missing

    def get_bom(self, did, wid, eid):
        '''
        Gets the tessellation of the edges of all parts in a part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''
        return self._api.request('get', '/api/assemblies/d/' + did + '/w/' + wid + '/e/' + eid + '/bom')

    def get_workspaces(self, did):
        '''
        Gets the workspace IDs.
        
        Args: 
            - did (str): Document ID

        Returns:
            - list of workspace ID
        '''

        # saves the request results into res
        res = self._api.request('get', '/api/documents/d/' + did + "/workspaces") #?noreadonly=false")
        
        # convert res into a json object before indexing into it on the next line
        res = res.json()
        
        wid = []
        ## Adding the loop
        for i in range(len(res)):
            wid.append(res[i]["id"])
        
        # extracts did from results dictionary
        #wid = res[0]["id"]
        return wid
        

    
    def element_list(self, did, w_list):
        '''
        Calls the "Element List" API call
        Gets a list of elements given a DID and list of WIDs
        
        Args: 
            - did (str): Document ID
            - w_list (str): list of Workspace ID

        Returns:
            - list of Element IDs
        ''' 
        '''
        e_dict = {}    
        for wid in w_list:
            res = self._api.request('get', '/api/documents/d/' + did + "/w/" + wid + "/elements")#?withThumbnails=false")
            # convert res into a json object before indexing into it on the next line
            res = res.json()
        
            eid = []

            for i in range(len(res)):
                eid.append(res[i]["id"])
            e_dict[wid] = eid
        '''
        eid_list = []
        element_type =[]

        for wid in w_list:
            res = self._api.request('get', '/api/documents/d/' + did + "/w/" + wid + "/elements")#?withThumbnails=false")
            # convert res into a json object before indexing into it on the next line
            res = res.json()

            # we go through each element and add it to list if it is not present
            for i in range(len(res)):
                eid = res[i]["id"]
                etype = res[i]["dataType"]
                if eid not in eid_list:
                    eid_list.append(eid)
                    element_type.append(etype)
        
        return eid_list, element_type

    def get_feature_list(self, did, wid, eid):
        '''
        Runs the Get Feature List API call. Requires DID, WID, and EID to be given
        
        Args: 
            - did, wid, eid, all as strings 

        Returns:
            - feature_count (int): a count of how many features there are in this element
            - feature_list (list): list of features, can include duplicates
        ''' 

        # list to store all the feature types from the response
        feature_types = []

        # makes Get Feature List API call using specified DID, WID, and EID
        res = self._api.request('get', '/api/partstudios/d/' + did + "/w/" + wid + "/e/" + eid + "/features")#?withThumbnails=false")
        # convert res into a json object before indexing into it on the next line
        #res = res.json()
        
        
        if res == 400:
            # if API call fails, then the WID and EID combo is no good. Return 0 as the count and the blank feature_types list
            feature_count = 0
            return feature_count, feature_types
        else:
            res = res.json()
        
            # count how many features there are, basically count the number of sub dictionaries there are in 
            # the "features" list in the API response
            feature_count = len(res["features"])

            # add each new feature type found to the list of feature types
            for i in range(feature_count):
                feature_types.append(res["features"][i]["message"]["featureType"])

            
            return feature_count, feature_types
            

    def get_parts_in_partstudio(self, did, wid, eid):
        # call "get parts in partstudio" API call given DID, WID, and EID

        res = self._api.request('get', '/api/parts/d/' + did + "/w/" + wid + "/e/" + eid)

        if res == 400:
            # if API call fails, then the WID and EID combo is no good. Return 0 as the count and the blank feature_types list
            count = 0
            return count
        else:
            res = res.json()
            try:
                count = len(res)
            except TypeError:
                count = 0
            return count #returns int of how many parts are in a partstudio tab eid

    def get_versions(self, did):

        res = self._api.request('get', '/api/documents/d/' + did + "/versions")

        if res == 400:
            # if API call fails, then the WID and EID combo is no good. Return 0 as the count and the blank feature_types list
            count = 0
            return count
        else:
            res = res.json()
            try:
                count = len(res)
            except TypeError:
                count = 0
            return count #returns int of how many versions there are in the did


    def get_asy_feature_list(self, did, wid, eid):
        '''
        ''' 
        # list to store all the feature types from the response
        asy_feature_types = []

        # makes Get Feature List API call using specified DID, WID, and EID
        res = self._api.request('get', '/api/assemblies/d/' + did + "/w/" + wid + "/e/" + eid + "/features")#?withThumbnails=false")
        # convert res into a json object before indexing into it on the next line
        #res = res.json()
        
        
        if res == 400:
            # if API call fails, then the WID and EID combo is no good. Return 0 as the count and the blank feature_types list
            feature_count = 0
            return feature_count, asy_feature_types
        else:
            res = res.json()
            feature_count = len(res["features"])
            for i in range(feature_count):
                try:
                    # Rename "circular" to "circular pattern" for better clarity
                    if res["features"][i]["typeName"] == "BTExplosion":
                        asy_feature_types.append("EXPLODED_VIEW")
                    elif res["features"][i]["message"]["parameters"][0]["message"]["value"] == "CIRCULAR":
                        asy_feature_types.append("CIRCULAR_PATTERN")
                    # Rename "on entity" to "mate connector" for better clarity
                    elif res["features"][i]["message"]["parameters"][0]["message"]["value"] == "ON_ENTITY":
                        asy_feature_types.append("MATE_CONNECTOR")
                    # both linear pattern and linear mate are the "linear" in the field I'm looking at,
                    #  this differentiates between the two
                    elif res["features"][i]["message"]["parameters"][0]["message"]["value"] == "LINEAR":
                        if res["features"][i]["message"]["parameters"][0]["message"]["enumName"] == "Pattern type":
                            asy_feature_types.append("LINEAR_PATTERN")
                        else:
                            asy_feature_types.append("LINEAR_MATE")
                    # if none of the special conditions apply, then just record the normal result 
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
                        print("\n\n\nA wild Assembly Feature Appeared\n\n\n")
                        asy_feature_types.append("UNACCOUNTED_ASY_FEATURE")
                except IndexError:
                    print("\n\n\nA wild Assembly Feature Appeared\n\n\n")
                    asy_feature_types.append("UNACCOUNTED_ASY_FEATURE")
            
            return feature_count, asy_feature_types

    def get_asy_instance_count(self, did, wid, eid):
        '''
        Calls the "Assemly Definition" API call
        ''' 
        # Calculates number of total instances, unique parts, linked parts, and # of sub-assemblies
        num_unique_parts = 0
        num_total_instances = 0
        num_linked_parts = 0
        num_sub_asms = 0


        # makes Get Feature List API call using specified DID, WID, and EID
        res = self._api.request('get', '/api/assemblies/d/' + did + "/w/" + wid + "/e/" + eid)#?withThumbnails=false")
        # convert res into a json object before indexing into it on the next line
        #res = res.json()
        
        
        if res == 400:
            # if API call fails. Return 0 for all three
            return num_unique_parts, num_total_instances, num_linked_parts, num_sub_asms
        else:
            res = res.json()
            try:
                num_unique_parts = len(res["parts"])
                num_total_instances = len(res["rootAssembly"]["instances"])
                num_sub_asms = len(res["subAssemblies"])

                #print("unique parts:", num_unique_parts)
                #print("total instances:", num_total_instances)
                #print("sub asms:", num_sub_asms)

                for i in range(num_unique_parts):
                    # checks if ths document ID of each part, if not the same as current DID, then it's an external part
                    if res["parts"][i]["documentId"] != did:
                        num_linked_parts += 1
            
                return num_unique_parts, num_total_instances, num_linked_parts, num_sub_asms


            except KeyError:
                print("\n\n\nkey error\n\n\n")
            except IndexError:
                print("\n\n\nindex error\n\n\n")