import json
from model.common.credential import Credential

class CredentialConverter(object):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''

    @staticmethod
    def to_json(credential):
        
        j_str = dict()
        
        j_str["username"] = credential.username
        j_str["password"] = credential.password
        
        j_str = json.dumps(j_str)
        
        return j_str
    
    @staticmethod
    def build_credential_from_json(j_str):
        
        credential = Credential()
        
        if not isinstance(j_str, dict):
            j_str  = json.loads(j_str)
        
        credential.username = j_str.pop("username", credential.username)
        credential.password = j_str.pop("password", credential.password)
        
        return credential