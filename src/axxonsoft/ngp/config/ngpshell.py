'''
Created on 24.01.2014

@author: anzor.apshev
'''

class NgpShell(object):
    def __init__(self, toolDir):
        """ tool_dir - specify dirrectory path to ngpsh tool """
        self.tool_dir = toolDir
        if (not os.path.exists(self._get_rsg_path())):
            raise RsgError("Can't find rsg tool. Path is invalid:%s" \
                           % self._get_rsg_path())
    