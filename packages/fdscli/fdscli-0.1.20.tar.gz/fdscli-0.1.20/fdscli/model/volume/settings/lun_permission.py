
class LunPermissions(object):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''
    
    def __init__(self, permissions="ro", lun_name=None):
        self.__lun_name = lun_name
        self.__permissions = permissions
        
    @property
    def permissions(self):
        return self.__permissions
    
    @permissions.setter
    def permissions(self, permissions):
        
        if permissions not in ("rw", "ro"):
            raise TypeError()
        
        self.__permissions = permissions
        
    @property
    def lun_name(self):
        return self.__lun_name
    
    @lun_name.setter
    def lun_name(self, a_name):
        self.__lun_name = a_name
        
