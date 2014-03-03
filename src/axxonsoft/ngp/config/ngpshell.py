'''
Created on 24.01.2014

@author: anzor.apshev
'''
import os
import subprocess
import shlex
import ngpstate


class NgpShellError(Exception):
    pass

def _parse_exec_mgr_status(line):
    words = line.split()
    return words[0], words[1]

class NgpShell(object):
    def __init__(self, tool_dir):
        """ tool_dir - specify dirrectory path to ngpsh tool """
        self.tool_dir = tool_dir
        if (not os.path.exists(self._get_ngpsh_path())):
            raise NgpShellError("Can't find rsg tool. Path is invalid:%s" \
                           % self._get_ngpsh_path())
    
    def repo_config_list(self):
        command_line = 'ngpsh.exe --command cfgrepo list'
        result = self._exec_tool(command_line)
        return set(result.split(os.linesep))
    
    def exec_manager_statuses(self):
        command_line = 'ngpsh.exe --command execmgr statuses'
        result = self._exec_tool(command_line)
        # Drop first line
        lines = result.split(os.linesep)[1:]
        # Parse each line
        results = dict(_parse_exec_mgr_status(line) for line  in lines)
        return ngpstate.ExecManagerStatuses(results)
    
    def trader_list(self):
        command_line = 'ngpsh.exe --command trader list'
        result = self._exec_tool(command_line)
        # Drop first line
        lines = result.split(os.linesep)[1:]
        # Parse each line
        return (line.split()[1] for line  in lines)
    
    def trader_query(self, type_name, quiet=False):
        command_line = 'ngpsh.exe --command trader query %s' % type_name
        result = self._exec_tool(command_line, quiet)
        # Drop first line
        lines = result.split(os.linesep)[1:]
        # Parse each line
        return [list(line.split()) for line in lines]
    
    def trader_query_all(self):
        results = dict((t, self.trader_query(t, True)) 
                       for t in self.trader_list())
        return ngpstate.Offers(results)

    def _exec_tool(self, command_line, quiet=False):
        if not quiet:
            print command_line
        args = shlex.split(command_line)
        try:
            return subprocess.check_output(args, executable=self._get_ngpsh_path()).strip()
        except subprocess.CalledProcessError as err:
            raise NgpShellError("Error occurred while executing ngpsh tool: %s " % err)
        
    def _get_ngpsh_path(self):
        return os.path.join(self.tool_dir, "ngpsh.exe")
    

    