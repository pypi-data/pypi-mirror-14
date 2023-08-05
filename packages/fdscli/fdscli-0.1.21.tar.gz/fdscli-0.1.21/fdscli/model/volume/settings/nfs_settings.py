from model.volume.settings.object_settings import ObjectSettings
from model.common.size import Size

class NfsSettings( ObjectSettings):
    '''
    Created on Nov 10, 2015
    
    @author: nate
    '''
    def __init__(self, use_acls=False, use_root_squash=False, synchronous=False, clients="*", max_object_size=None, capacity=Size( 1, "TB" ) ):
        self.type = "NFS"
        self.max_object_size = max_object_size
        self.__use_acls = use_acls
        self.__use_root_squash = use_root_squash
        self.__synchronous = synchronous
        self.__clients = clients
        self.__capacity = capacity
        
    def __convert_to_bool(self, value):
        
        if type( value ) is bool:
            return value
        
        if value.lower() in ( "true", "yes", "y", "t" ):
            return True
        
        return False
        
    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, cap):
        self.__capacity = cap
        
    @property
    def use_acls(self):
        return self.__use_acls
    
    @use_acls.setter
    def use_acls(self, acls):
        self.__use_acls = self.__convert_to_bool( acls )
        
    @property
    def use_root_squash(self):
        return self.__use_root_squash
    
    @use_root_squash.setter
    def use_root_squash(self, root_squash):
        self.__use_root_squash = self.__convert_to_bool( root_squash )
        
    @property
    def synchronous(self):
        return self.__synchronous
    
    @synchronous.setter
    def synchronous(self, sync):
        self.__synchronous= self.__convert_to_bool( sync )
        
    @property
    def clients(self):
        return self.__clients
    
    @clients.setter
    def clients(self, someClients):
        self.__clients = someClients