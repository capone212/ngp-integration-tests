'''
Created on 24.01.2014

@author: anzor.apshev
'''

import unittest
import platform

from rsg import RSGtool

class TestEnvirement(object):
    
    @staticmethod
    def getRsgPath():
        return r"D:\work\ngp_integration_stable\ngp\tools\rsg\bin\Release"
    
    @staticmethod
    def getLocalHostName():
        return  platform.node().upper()

class TestSequencedCreateDelete(unittest.TestCase): 
    def test_create_then_delete(self):
        rsg = RSGtool(TestEnvirement.getRsgPath())
        rsg.create(host=TestEnvirement.getLocalHostName(), objectType="Ipint",
                   initialParameters="Vendor=Axis;Model=P3301;LANAddress=192.168.200.88")
        
        
        