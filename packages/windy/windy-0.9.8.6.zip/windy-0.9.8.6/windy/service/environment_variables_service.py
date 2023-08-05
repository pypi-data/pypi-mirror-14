# -*- coding: utf-8 -*-
'''
Created on Feb 22, 2016

@author: zeljko.gavrilovic
'''

import winreg
import enum
    
class EnvironmentVariableService(object):
    """ This class is a service for CRUD operations on windows environment variables registry"""
    PATH_SEPARATOR = ';'
    
    def __init__(self, scope):
        self.scope = scope
        if scope is Scope.user:
            self.root = winreg.HKEY_CURRENT_USER
            self.subkey = Scope.user.value 
        else:
            self.root = winreg.HKEY_LOCAL_MACHINE
            self.subkey = Scope.system.value

    def getAllEnvVariable(self):
        result = []
        key = winreg.OpenKeyEx(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        for i in range(winreg.QueryInfoKey(key)[1]):
            name, value, envType = winreg.EnumValue(key, i)
            result.append((self.scope, name, value))
        winreg.CloseKey(key)    
        return result
    
    def getEnvVariable(self, name):
        key = winreg.OpenKeyEx(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        answer = winreg.QueryValueEx(key, name)
        result = (self.scope, name, answer[0])
        winreg.CloseKey(key)
        return result[2]

    def addEnvVariable(self, name, value):
        self.updateEnvVariable(name, value);

    def updateEnvVariable(self, name, value):
        if value:
            key = winreg.OpenKeyEx(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
            winreg.CloseKey(key)

    def removeEnvVariable(self, name):
        key = winreg.OpenKeyEx(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)

    def printVars(self, tuples):
        for t in tuples:
            self.printVar(t)

    def printVar(self, envTuple):
        print("%s = %s" % (envTuple[1], envTuple[2]))
        
class Scope(enum.Enum):
    user = 'Environment'
    system = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'       
        
""" improvised test, todo create a real unit test """
if __name__ == "__main__":
    wrs = EnvironmentVariableService("user")
    print("all user variables")
    wrs.printVars(wrs.getAllEnvVariable())

    print("TMP variable")
    wrs.printVar(wrs.getEnvVariable("TMP"))

    wrs.addEnvVariable("testDevEnv", r'c:\\dev')
    print("you should see the variable testDevEnv")
    wrs.printVars(wrs.getAllEnvVariable())
    
    wrs.updateEnvVariable("testDevEnv", r'c:\\dev\updated')
    print(r"you should see the variable testDevEnv=c:\\dev\updated")
    wrs.printVars(wrs.getAllEnvVariable())

    wrs.removeEnvVariable("testDevEnv")
    print("you should not see the variable testDevEnv")
    wrs.printVars(wrs.getAllEnvVariable())