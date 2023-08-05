
class Credential(object): 
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''
    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password
        
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, a_name):
        self.__username = a_name
        
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, a_password):
        self.__password = a_password