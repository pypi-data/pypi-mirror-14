from base_cli_test import BaseCliTest
from utils.converters.volume.settings_converter import SettingsConverter
import mock_functions
from mock import patch
from model.volume.settings.nfs_settings import NfsSettings
from utils.fds_cli_configuration_manager import FdsCliConfigurationManager
from model.common.size import Size
from boto.ec2.volume import Volume

class TestNfsVolume( BaseCliTest ):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''

    def test_marshalling(self):
        
        settings = NfsSettings()
        
        settings.use_acls = True
        settings.use_root_squash = False
        settings.synchronous = True
        
        settings.clients ="localhost*::[0-3]"
        
        j_str = SettingsConverter.to_json(settings)
        
        print( j_str )
        
        m_settings = SettingsConverter.build_settings_from_json( j_str )
        
        assert m_settings.type == "NFS"
        assert m_settings.clients == "localhost*::[0-3]"
        assert settings.use_acls is True
        assert settings.use_root_squash is False
        assert settings.synchronous is True
        
        # Checking the defaults
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 1, "Expected 1 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "TB", "Expected TB as a size unit but got {}".format( settings.capacity.unit )
        
        settings.capacity = Size( size=3, unit="EB" )
        
        j_str = SettingsConverter.to_json( settings )
        print( j_str )
        m_settings = SettingsConverter.build_settings_from_json(j_str)
        
        # Checking settings
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 3, "Expected 3 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "EB", "Expected EB as a size unit but got {}".format( settings.capacity.unit )
        
    @patch( "services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )        
    def test_nfs_creation(self, volumeCreate, listVolumes ):
        '''
        This test will make sure the settings look right after a volume create call
        '''
        print( "Testing NFS volume creation through the plugin with default size settings." )
        
        config = FdsCliConfigurationManager()
        
        self.cli.loadmodules()
        
        args = ['volume', 'create', '-name', 'nfs', '-type', 'nfs', '-acls', 'true', '-root_squash', 'false', 
                '-clients', '128.*2*.[6-9]::ab']
         
        self.callMessageFormatter(args)
        self.cli.run(args)
         
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
     
        assert settings.type == 'NFS'
        assert settings.clients == "128.*2*.[6-9]::ab"
        assert settings.use_acls is True
        assert settings.use_root_squash is False
        assert settings.synchronous is False
        
        # Checking the defaults
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 524288, "Expected 524288 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "GB", "Expected GB as a size unit but got {}".format( settings.capacity.unit )

        print( "Testing NFS volume creation through the plugin with explicit size settings." )
        
        args = ['volume', 'create', '-name', 'nfs', '-type', 'nfs', '-acls', 'false', '-root_squash', 'true', 
                '-clients', '228.*2*.[6-9]::ab', '-size', '243', '-size_unit', 'GB']
        
        self.callMessageFormatter(args)
        self.cli.run(args)
         
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
     
        assert settings.type == 'NFS'
        assert settings.clients == "228.*2*.[6-9]::ab"
        assert settings.use_acls is False
        assert settings.use_root_squash is True
        assert settings.synchronous is False
        
        # Checking the defaults
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 243, "Expected 243 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "GB", "Expected GB as a size unit but got {}".format( settings.capacity.unit )
        
    @patch( "services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getNfsVolume)
    @patch( "services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "services.volume_service.VolumeService.edit_volume", side_effect=mock_functions.editVolume )                 
    def test_nfs_edit(self, mock_edit, mock_list, mock_get_vol):
        '''
        This test will try to edit an NFS Volume
        '''
        
        print( "Testing the editing of an NFS volume" )
        
        config = FdsCliConfigurationManager()
        
        self.cli.loadmodules()
        
        args = ['volume', 'edit', '-volume_id', '3', '-clients', '10.1.1.1']
        
        self.callMessageFormatter(args)
        self.cli.run(args)
        
        volume = mock_edit.call_args[0][0]
        settings = volume.settings
        
        assert volume.id == 3
        assert settings.clients == '10.1.1.1'