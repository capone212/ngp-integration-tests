'''
Created on 24.01.2014

@author: anzor.apshev
'''
import os
import subprocess
import shlex


class NgpShellError(Exception):
    pass

class NgpShell(object):
    def __init__(self, tool_dir):
        """ tool_dir - specify dirrectory path to ngpsh tool """
        self.tool_dir = tool_dir
        if (not os.path.exists(self._get_ngpsh_path())):
            raise NgpShellError("Can't find rsg tool. Path is invalid:%s" \
                           % self._get_ngpsh_path())
    
    def repo_config_list(self):
        command_line = 'ngpsh.exe --command cfgrepo list'
        print command_line
        args = shlex.split(command_line)
        try:
            result = subprocess.check_output(args, executable=self._get_ngpsh_path()).strip()
            return result.split(os.linesep)
        except subprocess.CalledProcessError as err:
            raise NgpShellError("Error occurred while executing ngpsh tool: %s " % err)
        
    def _get_ngpsh_path(self):
        return os.path.join(self.tool_dir, "ngpsh.exe")