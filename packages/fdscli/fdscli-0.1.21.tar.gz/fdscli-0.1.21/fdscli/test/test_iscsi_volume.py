from base_cli_test import BaseCliTest
from model.volume.settings.iscsi_settings import ISCSISettings
from model.common.credential import Credential
from model.volume.settings.lun_permission import LunPermissions
from utils.converters.volume.settings_converter import SettingsConverter
import mock_functions
from mock import patch

class TestIscsiVolume( BaseCliTest ):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''

    def test_marshalling(self):
        
        settings = ISCSISettings()
        
        settings.initiators = ['me','you','them.*','him', 'her:']
        settings.incoming_credentials = [
            Credential( username='Bob',password='Test'),
            Credential( username='Phyllis',password='Toast')
                                         ]
        
        settings.outgoing_credentials = [
            Credential( username='Mack',password='Fires'),
            Credential( username='Mort',password='trom')
                                         ]
        
        settings.lun_permissions = [LunPermissions(lun_name="1", permissions="ro")]
        
        j_str = SettingsConverter.to_json(settings)
        
        print( j_str )
        
        m_settings = SettingsConverter.build_settings_from_json( j_str )
        
        assert m_settings.type == "ISCSI"
        assert len( m_settings.incoming_credentials ) == 2
        assert len( m_settings.outgoing_credentials ) == 2
        assert len( m_settings.initiators ) == 5
        assert "them.*" in m_settings.initiators
        assert "her:" in m_settings.initiators
        assert m_settings.lun_permissions[0].lun_name == "1" and m_settings.lun_permissions[0].permissions == "ro"
     
    @patch( "services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )        
    def test_iscsi_creation_defaults(self, volumeCreate, listVolumes ):
        '''
        This test will make sure the settings look right after a volume create call
        '''
        
        args = ['volume', 'create', '-name', 'iscsi', '-type', 'iscsi']

        self.callMessageFormatter(args)
        self.cli.run(args)
        
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
    
        assert settings.type == 'ISCSI'
        assert len( settings.initiators ) == 0
        assert len( settings.lun_permissions ) == 0
        assert len( settings.incoming_credentials ) == 0
        assert len( settings.outgoing_credentials ) == 0
        assert settings.capacity.size == 524288
        assert settings.capacity.unit == 'GB'   
        
    @patch( "services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )        
    def test_iscsi_creation(self, volumeCreate, listVolumes ):
        '''
        This test will make sure the settings look right after a volume create call
        '''
        
        args = ['volume', 'create', '-name', 'iscsi', '-type', 'iscsi', '-initiators', 'he:', 'me.*', 'him', 'her', '-incoming_credentials', 'user:test', 'user2:three', 
                '-outgoing_credentials', 'fourth:one', '-lun_permissions', '0:ro', '1:rw', '-size', '2', '-size_unit', 'TB']
        
        self.callMessageFormatter(args)
        self.cli.run(args)
        
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
    
        assert settings.type == 'ISCSI'
        assert len( settings.initiators ) == 4
        assert settings.initiators[0] in ('he:', 'me.*', 'him', 'her')
        assert settings.initiators[1] in ('he:', 'me.*', 'him', 'her')
        assert settings.initiators[2] in ('he:', 'me.*', 'him', 'her')
        assert settings.initiators[3] in ('he:', 'me.*', 'him', 'her')
        assert len( settings.lun_permissions ) == 2
        assert len( settings.incoming_credentials ) == 2
        assert len( settings.outgoing_credentials ) == 1
        assert settings.outgoing_credentials[0].username == 'fourth'
        assert settings.outgoing_credentials[0].password == 'one'
        assert settings.capacity.size == 2
        assert settings.capacity.unit == 'TB'
        
        