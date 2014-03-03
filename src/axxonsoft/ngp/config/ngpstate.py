'''
Created on 27.02.2014

@author: anzor.apshev
'''
import json
import axxonsoft

class NgpState(object):
    '''
        Represents NGP server state, such as configuration,
        active objects and so on. 
    '''
    @classmethod
    def from_ngp_shell(cls, ngp_shell):
        return NgpState(ngp_shell.repo_config_list(),
                      ngp_shell.exec_manager_statuses(),
                      ngp_shell.trader_query_all())
    
    def __init__(self, cfg_list, statuses, offers):
        self.cfg_list = cfg_list
        self.statuses = statuses
        self.offers = offers
    
    def difference(self, other):
        if not isinstance(other, self.__class__):
            raise RuntimeError("Wrong type")
        return NgpState(self.cfg_list.difference(other.cfg_list),
                        self.statuses.difference(other.statuses),
                        self.offers.difference(other.offers))
    
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        tmp = {'cfg_list' : str(self.cfg_list), 
               'statuses' : str(self.statuses),
               'offers' : str(self.offers)}
        return str(tmp)



class Offers(object):
    def __init__(self, offers):
        self.offers = offers
        
    def _list_diff(self, list1, list2):
        return [x for x in list1 if x not in list2]
        
    
    def difference(self, other):
#        if not isinstance(other, self.__class__):
#            raise RuntimeError("Wrong type")
        difftmp = dict()
        for k, v in self.offers.items():
            if k in other.offers:
                difftmp[k] = self._list_diff(v, other.offers[k])
            else:
                difftmp[k] = v
        return Offers(difftmp)
        
#        return Offers(dict([(k, v) for k, v in self.offers.items() 
#            if (k not in other.offers) or (other.offers[k] != v)]))
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for k, v in self.offers.items():
            if  k not in other.offers or len(other.offers[k]) != len(v) :
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return str(self.offers)
        

class ExecManagerStatuses(object):
    def __init__(self, statusesDictionary):
        values = statusesDictionary.values()
        EQUAL_STATUSES = {'STARTING' : 'STARTED', 'STOPPING' : 'STOPPED' }
        values = self._replace(values, EQUAL_STATUSES)
        self.statuses = dict(zip(statusesDictionary.keys(),values))
    
    def difference(self, other):
        #if not isinstance(other, self.__class__):
        #    raise RuntimeError("Wrong type. true type %s wrong type %s" %
         #                      (self.__class__, other.__class__))
        return ExecManagerStatuses(dict(set(self.statuses.items())
                         - set(other.statuses.items())))
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other) 
        
    
    def _replace(self, values, sdict):
        return [sdict[x] if x in sdict else x for x in values ]
    
    def __str__(self):
        return str(self.statuses)
    
    
class NgpStateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NgpState):
            return {'cfg_list' : obj.cfg_list, 
                    'statuses' : obj.statuses,
                    'offers' : obj.offers}
        if isinstance(obj, Offers):
            return obj.offers
        if isinstance(obj, ExecManagerStatuses):
            return obj.statuses
        if isinstance(obj, set):
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode  ):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv
    
    
def as_NgpState(json_dct):
    json_dct = _decode_dict(json_dct)
    if not 'cfg_list' in json_dct:
        return json_dct
    cfg_list = set(json_dct['cfg_list'])
    statuses = ExecManagerStatuses(json_dct['statuses'])
    offers = Offers(json_dct['offers'])
    return NgpState(cfg_list, statuses, offers)    
    