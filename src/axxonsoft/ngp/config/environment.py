'''
Created on 26.02.2014

@author: anzor.apshev
'''
import platform
import os
import shlex
import subprocess
import time

class TestEnvirement(object):
    
    @staticmethod
    def getRsgDirectory():
        return r"D:\temp\itest"
        #return r"C:\Program Files (x86)\AxxonSoft\AxxonSmart\bin"
    
    @staticmethod
    def getNgpShellDirrectory():
        return r"C:\Program Files (x86)\AxxonSoft\AxxonSmart\bin"
    
    @staticmethod
    def getLocalHostName():
        return  platform.node().upper()

class CleanConfigurationError(Exception):
    pass

def clean_ngp_configuration():  
    clean_script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     "ZeroConfig.bat")
    print clean_script_path
    print "Cleaning NGP configuration up ..."
    try:
        subprocess.check_output(clean_script_path, shell=True, stderr=None)
        time.sleep(10)
        print "Clean up OK."
    except subprocess.CalledProcessError as err:
        raise CleanConfigurationError("Error occurred while executing clean tool: %s " % err)