'''
Created on 27.02.2014

@author: anzor.apshev
'''
   
class NgpState(object):
    '''
        Represents NGP server state, such as configuration,
        active objects and so on. 
    '''
    pass


class ExecManagerStatuses(object):
    def __init__(self, statusesDictionary):
        values = statusesDictionary.values()
        EQUAL_STATUSES = {'STARTING' : 'STARTED', 'STOPPING' : 'STOPPED' }
        values = self._replace(values, EQUAL_STATUSES)
        self.statuses = statusesDictionary.fromkeys(values)
    
    def difference(self, other):
        if not isinstance(other, self.__class__):
            raise RuntimeError("Wrong type")
        return set(self.statuses.items()) - set(other.statuses.items())
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other) 
        
    
    def _replace(self, values, sdict):
        return [sdict[x] if x in sdict else x for x in values ]
    
    