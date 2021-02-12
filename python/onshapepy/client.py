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
        Gets the tessellation of the edges of all parts in a part studio.

        Args:
            - did (str): Document ID
            - wid (str): Workspace ID
            - eid (str): Element ID

        Returns:
            - requests.Response: Onshape response data
        '''
        return self._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/massproperties')

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
        

    
    def get_elements(self, did, w_list):
        '''
        Gets the workspace ID.
        
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
        for wid in w_list:
            res = self._api.request('get', '/api/documents/d/' + did + "/w/" + wid + "/elements")#?withThumbnails=false")
            # convert res into a json object before indexing into it on the next line
            res = res.json()

            # we go through each element and add it to list if it is not present
            for i in range(len(res)):
                eid = res[i]["id"]
                if eid not in eid_list:
                    eid_list.append(eid)

        return eid_list