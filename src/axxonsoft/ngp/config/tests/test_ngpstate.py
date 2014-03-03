'''
Created on 27.02.2014

@author: anzor.apshev
'''

import unittest
from axxonsoft.ngp.config.ngpstate import ExecManagerStatuses
from axxonsoft.ngp.config.ngpstate import Offers
from axxonsoft.ngp.config.ngpstate import NgpState
from axxonsoft.ngp.config.ngpstate import NgpStateEncoder
from axxonsoft.ngp.config.ngpstate import as_NgpState
import json

class TestExecManagerStatuses(unittest.TestCase):
    def test_not_equal(self):
        value1 = {'name1':'STARTED', 'name2':'STARTED', 'name3':'STOPPED'}
        value2 = {'name1':'STOPPED', 'name2':'STARTED', 'name3':'STOPPED'}
        self.assertNotEqual(ExecManagerStatuses(value1), 
                            ExecManagerStatuses(value2), "Should not be equal")
        
    def test_equal(self):
        value1 = {'name1':'STARTED', 'name2':'STOPPED'}
        value2 = {'name1':'STARTING', 'name2':'STOPPED'}
        self.assertEqual(ExecManagerStatuses(value1), 
                            ExecManagerStatuses(value2), "Should be equal")
    
    def test_difference(self):
        value1 = ExecManagerStatuses({'name1':'STOPPED', 'name2':'STOPPED'})
        value2 = ExecManagerStatuses({'name1':'STARTING', 'name2':'STOPPED'})
        diff = value1.difference(value2)
        self.assertEqual(diff, ExecManagerStatuses({'name1':'STOPPED'}), "Should be equal")
        
class TestOffers(unittest.TestCase):
    def test_difference(self):
        offers = Offers({'Offer1':[[1,'hello',3],[2,'hello',4]],
                      'Offer2':[['hello','yes'],['hello2','no']]})
        offers2 = Offers({'Offer1':[[1,'hello',3],[2,'hello',4]]})
        diff = offers.difference(offers2)
        self.assertEqual(diff, Offers({'Offer1': [],
                                       'Offer2': [['hello', 'yes'], ['hello2', 'no']]}),
                         "Should be the same")
    

class TestNgpState(unittest.TestCase):
    def test_json_serialization(self): 
        cfg_list = set(['Service 1', 'Service 2', 'Service 3'])
        statuses = ExecManagerStatuses({'name1':'STOPPED', 'name2':'STOPPED'})
        offers = Offers({'Offer1':[[1,'hello',3],[2,'hello',4]],
                         'Offer2':[['hello','yes'],['hello2','no']]
                                   })
        state = NgpState(cfg_list, statuses, offers)
        str_buffer = json.dumps(state, cls=NgpStateEncoder)
        state_loaded = json.loads(str_buffer, 
                                  object_hook=as_NgpState)
        self.assertEqual(state, state_loaded, 
                "Should be equal. Diff: %s" % state.difference(state_loaded))
        
        
        

if __name__ == '__main__':
    unittest.main()        