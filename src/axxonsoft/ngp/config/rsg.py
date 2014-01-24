'''
Created on 24.01.2014

@author: anzor.apshev
'''

import os
import subprocess
import shlex
import json

class RsgError(Exception):
    pass

class RSGtool(object):
    
    def __init__(self, tool_dir, host_name):
        """ tool_dir - specify dirrectory path to rsg tool """
        self.tool_dir = tool_dir
        if (not os.path.exists(self._get_rsg_path())):
            raise RsgError("Can't find rsg tool. Path is invalid:%s" \
                           % self._get_rsg_path())
        self.host_name = host_name
            
            
    def create(self, objectType, initialParameters):
        """ Creates new ngp object 
            
            arguments
            host - remote host address
            objectType - NGP object type to create
            initialParameters - initial parameters for creating object
        """
        command_line = 'rsg create -ot="%s" -pl="%s" -ht="%s"' % (
                        objectType, initialParameters, self.host_name)
        return self._execTool(command_line)

    def delete(self, objectType, objectId):
        command_line = 'rsg delete -ot="%s" -id="%s" -ht="%s"' % (
                        objectType, objectId, self.host_name)
        return self._execTool(command_line)
    
    def list(self, objectType, showChilds=False, showSettings=False):
        command_line = 'rsg list -ot="%s" -ht="%s" %s %s' % (
                                objectType, self.host_name,
                                "-ch" if showChilds else "",
                                "-st" if showSettings else "")
        result = self._execTool(command_line)
        return json.loads(result)
           
    
    def _execTool(self, command_line):
        print command_line
        args = shlex.split(command_line)
        try:
            return subprocess.check_output(args, executable=self._get_rsg_path())
        except subprocess.CalledProcessError as err:
            raise RsgError("Error occurred while executing rsg tool: %s " % err)
                    
        
    def _get_rsg_path(self):
        return os.path.join(self.tool_dir, "rsg.exe")