'''
Created on Dec 22, 2015

@author: nate
'''
from __future__ import division
from xdrlib import ConversionError

class ByteConverter(object):
    '''
    This class will convert size objects into a reasonable string representation
    '''
    KB = 1024
    MB = KB*KB
    GB = MB*KB
    TB = GB*KB
    PB = TB*KB
    EB = PB*KB
    
    byteStr = "bytes"
    kbStr = "KB"
    mbStr = "MB"
    gbStr = "GB"
    tbStr = "TB"
    pbStr = "PB"
    ebStr = "EB"
    
    @staticmethod
    def convertBytesToString( byte_value=0, decimal_places=2):
        '''
        Take some bytes and turn them into a nice printable string with units
        '''
        num_value = byte_value
        unit_value = ByteConverter.byteStr
        
        if byte_value < ByteConverter.KB:
            num_value = byte_value
            unit_value = ByteConverter.byteStr
        elif  byte_value < ByteConverter.MB:
            num_value = byte_value/ByteConverter.KB 
            unit_value = ByteConverter.kbStr;
        elif byte_value < ByteConverter.GB:
            num_value = byte_value / ByteConverter.MB
            unit_value = ByteConverter.mbStr;
        elif byte_value < ByteConverter.TB:
            num_value = byte_value / ByteConverter.GB 
            unit_value = ByteConverter.gbStr;
        elif byte_value < ByteConverter.PB:
            num_value = byte_value / ByteConverter.TB
            unit_value = ByteConverter.tbStr;
        elif byte_value < ByteConverter.EB:
            num_value = byte_value / ByteConverter.PB
            unit_value = ByteConverter.pbStr;
        else:
            num_value = byte_value / ByteConverter.EB
            unit_value = ByteConverter.ebStr;

        s = "{} {}".format( round( num_value, decimal_places ), unit_value )
        
        if unit_value == ByteConverter.byteStr:
            s = "{} {}".format( num_value, unit_value )
            
        return s
    
    @staticmethod
    def convertSizeToString( size=0, units="B", decimal_places=2):
        '''
        This method will take a unit value and then do the conversion
        to the most visually appealing number it can.
        '''
        num_bytes = size
        
        if units == ByteConverter.kbStr:
            num_bytes *= ByteConverter.KB
        elif units == ByteConverter.mbStr:
            num_bytes *= ByteConverter.MB
        elif units == ByteConverter.gbStr:
            num_bytes *= ByteConverter.GB
        elif units == ByteConverter.tbStr:
            num_bytes *= ByteConverter.TB
        elif units == ByteConverter.pbStr:
            num_bytes *= ByteConverter.PB
        elif units == ByteConverter.ebStr:
            num_bytes *= ByteConverter.EB
            
        return ByteConverter.convertBytesToString( num_bytes, decimal_places )
        