'''
Created on 24.01.2014

@author: anzor.apshev
'''

import unittest
import environment
from rsg import RSGtool
from ngpshell import NgpShell
from environment import TestEnvirement

class TestSequencedCreateDelete(unittest.TestCase):
    
    def setUp(self):
        environment.clean_ngp_configuration()
        pass
    
    def test_01_create_then_delete(self):
        ngp_shell = NgpShell(TestEnvirement.getNgpShellDirrectory())
        initial_cfg_list = ngp_shell.repo_config_list()
        initial_statuses = ngp_shell.exec_manager_statuses()
        initial_offers = ngp_shell.trader_query_all()
        
        # Create new ipint object
        rsg = RSGtool(TestEnvirement.getRsgDirectory(), 
                      TestEnvirement.getLocalHostName())
        rsg.create(objectType="Ipint", initialParameters=
                   "Vendor=Axis;Model=P3301;LANAddress=192.168.200.88")
        
        # Validate new objects created
        self.assertGreater(len(ngp_shell.repo_config_list()),
                           len(initial_cfg_list), 
                           "New objects should be created by create command.")
        
        ipintObjects = rsg.list("Ipint")
        self.assertEqual(len(ipintObjects), 1,
                         "There should be only one IPINT object.")
        # Delete instantiated device
        rsg.delete("Ipint", ipintObjects[0]['id'])
        
        # Validate list before and after is equal 
        post_cfg_list = ngp_shell.repo_config_list()
        post_statuses = ngp_shell.exec_manager_statuses()
        post_offers = ngp_shell.trader_query_all()
        
        self.assertEqual(initial_cfg_list, post_cfg_list,
                         "Objects lists before and after have to be equal. \
                         This objects are seems orphaned: %s." %  (
                                set(post_cfg_list) - set(initial_cfg_list)))
        
        self.assertEqual(initial_statuses, post_statuses,
            "Objects statuses should be the same.\
            These objects seems in invalid state: %s." %
            post_statuses.difference(initial_statuses))
        
        self.assertEqual(initial_offers, post_offers,
                         "Published offers should be the same \
                         before and after. Mismatch offers %s" % 
                         post_offers.difference(initial_offers))

if __name__ == '__main__':
    unittest.main()    