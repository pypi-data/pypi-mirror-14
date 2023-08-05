import os
import sys
import cmd
import shlex
import pipes
from argparse import ArgumentParser
import pkgutil

sys.path.append( os.path.dirname( os.path.abspath( __file__ ) ) )

def main():
    
    from services.fds_auth import FdsAuth
    from FDSShell import FDSShell
    from utils.fds_cli_configuration_manager import FdsCliConfigurationManager
    
    cmdargs=sys.argv[1:]

    if ( len(cmdargs) > 0 and str(cmdargs[0]).startswith( "-conf_file" ) ):

        conf_file = None
        equalsSign = cmdargs[0].find( "=" )
        
        if ( equalsSign == -1 ):
            conf_file = cmdargs[1]
            cmdargs=cmdargs[2:]
        else:
            conf_file = cmdargs[0][equalsSign+1:]
            cmdargs=cmdargs[1:]
            
        FdsCliConfigurationManager( ["conf_file="+conf_file])
    #fi
    
    auth = FdsAuth()

    shell = FDSShell(auth, cmdargs)

    # now we check argv[0] to see if its a shortcut scripts or not
    if ( len( cmdargs ) > 0 ):

        for plugin in shell.plugins:
            detectMethod = getattr( plugin, "detect_shortcut", None )

            # the plugin does not support shortcut argv[0] stuff
            if ( detectMethod is None or not callable( plugin.detect_shortcut ) ):
                continue

            tempArgs = plugin.detect_shortcut( cmdargs )

            # we got a new argument set
            if ( tempArgs is not None ):
                cmdargs = tempArgs
                break
        # end of for loop

    # now actually run the command
    shell.run ( cmdargs )

if __name__ == '__main__':
    main()
