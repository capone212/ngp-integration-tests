'''
Created on 27.02.2014

@author: anzor.apshev
'''

import unittest
from axxonsoft.ngp.config.ngpstate import ExecManagerStatuses

class TestExecManagerStatuses(unittest.TestCase):
    def test_not_equal(self):
        value1 = {'name1':'STARTED', 'name2':'STOPPED'}
        value2 = {'name1':'STOPPED', 'name2':'STOPPED'}
        self.assertNotEqual(ExecManagerStatuses(value1), 
                            ExecManagerStatuses(value2), "Should not be equal")
        
    def test_equal(self):
        value1 = {'name1':'STARTED', 'name2':'STOPPED'}
        value2 = {'name1':'STARTING', 'name2':'STOPPED'}
        self.assertEqual(ExecManagerStatuses(value1), 
                            ExecManagerStatuses(value2), "Should not be equal")
        

if __name__ == '__main__':
    unittest.main()        