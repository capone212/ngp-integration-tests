'''
Created on 24.01.2014

@author: anzor.apshev
'''

import unittest
import platform
from multiprocessing import Pool
import re

from rsg import RSGtool
from ngpshell import NgpShell

class TestUtilsException(Exception):
    pass

# class TestUtils(object):
#     @staticmethod
#     def assertGreater(first, second, message):
#         if not (first > second):
#             raise TestUtilsException(message)
#     
#     @staticmethod
#     def assertEqual(first, second, message):
#         if not (first == second):
#             raise TestUtilsException(message)
#     
        

def runSingleThread(workerID):    
    # Create new ipint object
    rsg = RSGtool(TestEnvirement.getRsgDirectory(), TestEnvirement.getLocalHostName())
    rsg.create(objectType="Ipint",
               initialParameters=("Vendor=Axis;Model=P3301;LANAddress=192.168.200.88;DisplayId=%s" % workerID))
    
    ipintObjects = rsg.list("Ipint")
    
    createdIpDevice = next(deviceRecord for deviceRecord in ipintObjects 
         if re.match((".+/DeviceIpint.%s" % workerID), deviceRecord['id']))
    
    # Delete instantiated device
    rsg.delete("Ipint", createdIpDevice['id'])
    

class TestEnvirement(object):
    
    @staticmethod
    def getRsgDirectory():
        return r"D:\work\ngp_integration_test\tools\rsg\bin\Debug"
        #return r"C:\Program Files (x86)\AxxonSoft\AxxonSmart\bin"
    
    @staticmethod
    def getNgpShellDirrectory():
        return r"C:\Program Files (x86)\AxxonSoft\AxxonSmart\bin"
    
    @staticmethod
    def getLocalHostName():
        return  platform.node().upper()

@unittest.skip("Is not ready yet")
class TestSequencedCreateDelete(unittest.TestCase): 
    def _01_create_then_delete(self):
        ngpShell = NgpShell(TestEnvirement.getNgpShellDirrectory())
        initialObjectsList = ngpShell.repo_config_list()
        
        # Create new ipint object
        rsg = RSGtool(TestEnvirement.getRsgDirectory(), TestEnvirement.getLocalHostName())
        rsg.create(objectType="Ipint",
                   initialParameters="Vendor=Axis;Model=P3301;LANAddress=192.168.200.88")
        
        # Validate new objects created
        self.assertGreater(len(ngpShell.repo_config_list()), len(initialObjectsList), 
                           "New objects should be created by create command.")
        
        ipintObjects = rsg.list("Ipint")
        self.assertEqual(len(ipintObjects), 1, "There should be only one IPINT object.")
        # Delete instantiated device
        rsg.delete("Ipint", ipintObjects[0]['id'])
        
        # Validate list before and after is equal 
        postObjectsCondition = ngpShell.repo_config_list()
        
        self.assertEqual(initialObjectsList, postObjectsCondition,
                         "Objects lists before and after have to be equal. This objects are seems orphaned: %s." %  (
                                set(postObjectsCondition) - set(initialObjectsList)))
        
    
    def test_02_multithreaded_create_and_delete(self):
        ngpShell = NgpShell(TestEnvirement.getNgpShellDirrectory())
        initialObjectsList = ngpShell.repo_config_list()
        
        p = Pool(processes = 5)
        p.map(runSingleThread, range(5))
        
        # Validate list before and after is equal 
        postObjectsCondition = ngpShell.repo_config_list()
        self.assertEqual(initialObjectsList, postObjectsCondition,
                         "Objects lists before and after have to be equal. This objects are seems orphaned: %s." %  (
                                set(postObjectsCondition) - set(initialObjectsList)))
        
        
        