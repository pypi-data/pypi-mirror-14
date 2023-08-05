import json
from model.volume.settings.lun_permission import LunPermissions

class LunPermissionConverter(object):    
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''
    @staticmethod
    def to_json( lun_permission ):
        
        j_str = dict()
        
        j_str["lunName"] = lun_permission.lun_name
        j_str["accessType"] = lun_permission.permissions.upper()
        
        j_str = json.dumps( j_str )
        
        return j_str
    
    @staticmethod
    def build_lun_permission_from_json( j_str ):
        
        lun_permission = LunPermissions()
        
        if not isinstance(j_str, dict):
            j_str  = json.loads(j_str)
        
        lun_permission.lun_name = j_str["lunName"]
        lun_permission.permissions = j_str["accessType"].lower()
        
        return lun_permission