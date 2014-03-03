'''
Created on 26.02.2014

@author: anzor.apshev
'''
import os
import unittest
import environment
import json
import ngpstate
from rsg import RSGtool
from ngpshell import NgpShell
from environment import TestEnvirement


class TestCreate(unittest.TestCase):
    
    def setUp(self):
        environment.clean_ngp_configuration()
        pass
    
    def test_single_channel(self):
        
        ngp_shell = NgpShell(TestEnvirement.getNgpShellDirrectory())        
        initial_state = ngpstate.NgpState.from_ngp_shell(ngp_shell)
        
        # Create new ipint object
        rsg = RSGtool(TestEnvirement.getRsgDirectory(), 
                      TestEnvirement.getLocalHostName())
        rsg.create(objectType="Ipint", initialParameters=
            "Vendor=ONVIF;Model=1_channel_device;LANAddress=192.168.200.88")
        post_state = ngpstate.NgpState.from_ngp_shell(ngp_shell)
        
        diff = post_state.difference(initial_state)
        etalon = _load_etalon()
        self.assertEquals(diff, etalon, 
                          "Should be equal! %s" % diff.difference(etalon))
        

        
def _load_etalon():
    file_name = os.path.join(os.path.dirname(__file__), 
                             r'data\create_onvif_1_channel_state_diff.json')
    state = json.load(open(file_name), object_hook=ngpstate.as_NgpState)
    return state        
        
    
if __name__ == '__main__':
    unittest.main()
#    status = _load_etalon()
#    print status.__class__
#    print status.cfg_list
#    print status.statuses
#    print status.offers
      