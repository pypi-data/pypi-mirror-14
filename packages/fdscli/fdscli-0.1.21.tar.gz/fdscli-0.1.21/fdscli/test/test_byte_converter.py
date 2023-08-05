'''
Created on Jan 20, 2016

@author: nate
'''
from base_cli_test import BaseCliTest
from utils.byte_converter import ByteConverter


class Test(BaseCliTest):


    def test_converstions(self):
        
        s = ByteConverter.convertBytesToString( byte_value=4507997673881, decimal_places=2 )
        
        assert s == "4.1 TB", "Expected 4.1 TB but got: {}".format( s )
        
        s = ByteConverter.convertBytesToString( byte_value=4707997673881, decimal_places=2 )
        
        assert s == "4.28 TB", "Expected 4.28 TB but got: {}".format( s )
        
        s = ByteConverter.convertBytesToString( byte_value=0, decimal_places=2 )
        
        assert s == "0 bytes", "Expected 0 bytes but got: {}".format( s )
        
        s = ByteConverter.convertBytesToString( byte_value=145, decimal_places=2 )
        
        assert s == "145 bytes", "Expected 145 bytes but got: {}".format( s )
        
        s = ByteConverter.convertBytesToString( byte_value=1124, decimal_places=2 )
        
        assert s == "1.1 KB", "Expected 1.1 KB but got: {}".format( s )
        
        s = ByteConverter.convertBytesToString( byte_value=1234567, decimal_places=2 )
        
        assert s == "1.18 MB", "Expected 1.18 MB but got: {}".format( s )        