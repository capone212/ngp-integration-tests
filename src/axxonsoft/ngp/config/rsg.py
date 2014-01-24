'''
Created on 24.01.2014

@author: anzor.apshev
'''

import os
import subprocess
import shlex

class RsgError(Exception):
    pass

class RSGtool(object):
    
    def __init__(self, toolDir):
        """ tool_dir - specify dirrectory path to rsg tool """
        self.tool_dir = toolDir
        if (not os.path.exists(self._get_rsg_path())):
            raise RsgError("Can't find rsg tool. Path is invalid:%s" \
                           % self._get_rsg_path())
            
            
    def create(self, host, objectType, initialParameters):
        """ Creates new ngp object 
            
            arguments
            host - remote host address
            objectType - NGP object type to create
            initialParameters - initial parameters for creating object
        """
        command_line = 'rsg create -ot="%s" -pl="%s" -h="%s"' % (
                        objectType,
                        initialParameters,
                        host)
        print command_line
        args = shlex.split(command_line)
        try:
            return subprocess.check_output(args, executable=self._get_rsg_path())
        except subprocess.CalledProcessError as err:
            raise RsgError("Error occurred while executing rsg tool: %s " % err)
                    
        
    def _get_rsg_path(self):
        return os.path.join(self.tool_dir, "rsg.exe")