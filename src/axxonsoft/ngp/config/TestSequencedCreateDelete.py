'''
Created on 24.01.2014

@author: anzor.apshev
'''

import unittest
import platform

from rsg import RSGtool
from ngpshell import NgpShell

class TestEnvirement(object):
    
    @staticmethod
    def getRsgDirectory():
        return r"D:\work\ngp_integration_test\tools\rsg\bin\Release"
    
    @staticmethod
    def getNgpShellDirrectory():
        return r"C:\Program Files (x86)\AxxonSoft\AxxonSmart\bin"
    
    @staticmethod
    def getLocalHostName():
        return  platform.node().upper()

class TestSequencedCreateDelete(unittest.TestCase): 
    def test_create_then_delete(self):
        # Save initial objects list
        ngpShell = NgpShell(TestEnvirement.getNgpShellDirrectory())
        initialObjectsList = ngpShell.repo_config_list()
        
        # Create new ipint object
        rsg = RSGtool(TestEnvirement.getRsgDirectory(), TestEnvirement.getLocalHostName())
        rsg.create(objectType="Ipint",
                   initialParameters="Vendor=Axis;Model=P3301;LANAddress=192.168.200.88")
        
        # Validate new objects created
        self.assertGreater(len(ngpShell.repo_config_list()), len(initialObjectsList), 
                           "New objects should be created by create command")
        
        ipintObjects = rsg.list("Ipint")
        self.assertEqual(len(ipintObjects), 1, "There should be only one IPINT object")
        # Delete instantiated device
        rsg.delete("Ipint", ipintObjects[0]['id'])
        
        # Validate list before and after is equal 
        postObjectsCondition = ngpShell.repo_config_list()
        
        self.assertListEqual(initialObjectsList, postObjectsCondition,
                         "Objects lists before and after have to be equal. This objects are seems orphaned: %s" %  (
                                set(postObjectsCondition) - set(initialObjectsList)))
        
        
        