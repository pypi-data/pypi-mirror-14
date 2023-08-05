from model.volume.settings.block_settings import BlockSettings
from model.common.size import Size


class ISCSISettings(BlockSettings):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''
    def __init__(self, capacity=Size(10, "GB"), block_size=None):
        self.type = "ISCSI"
        self.capacity = capacity
        self.block_size = block_size
        self.__incoming_credentials = []
        self.__outgoing_credentials = []
        self.__lun_permissions = []
        self.__initiators = []
        
    @property
    def incoming_credentials(self):
        return self.__incoming_credentials
    
    @incoming_credentials.setter
    def incoming_credentials(self, credentials):
        self.__incoming_credentials = credentials;
        
    @property
    def outgoing_credentials(self):
        return self.__outgoing_credentials
    
    @outgoing_credentials.setter
    def outgoing_credentials(self, credentials):
        self.__outgoing_credentials = credentials
        
    @property
    def lun_permissions(self):
        return self.__lun_permissions
    
    @lun_permissions.setter
    def lun_permissions(self, permissions):
        self.__lun_permissions = permissions
        
    @property
    def initiators(self):
        return self.__initiators
    
    @initiators.setter
    def initiators(self, some_initiators):
        self.__initiators = some_initiators
