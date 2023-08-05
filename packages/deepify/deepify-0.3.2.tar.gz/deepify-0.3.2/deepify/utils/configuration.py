# !/usr/bin/python
# -*- coding: utf-8 -*-
#
##################################################################################
#
#    Copyright 2016 Félix Brezo and Yaiza Rubio (i3visio, contacto@i3visio.com)
#
#    This file is part of Deepify. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

import ConfigParser

import os
import sys

def changePermissionsRecursively(path, uid, gid):
    """
        Function to recursively change the user id and group id. It sets 700 
        permissions.
    """
    os.chown(path, uid, gid)
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isfile(itempath):
            # Setting owner
            try:
                os.chown(itempath, uid, gid)
            except Exception, e:
                # If this crashes it may be because we are running the 
                # application in Windows systems, where os.chown does NOT work.
                pass
            # Setting permissions
            os.chmod(itempath, 0600) 
        elif os.path.isdir(itempath):
            # Setting owner
            try:
                os.chown(itempath, uid, gid)
            except Exception, e:
                # If this crashes it may be because we are running the 
                # application in Windows systems, where os.chown does NOT work.
                pass
            # Setting permissions
            os.chmod(itempath, 6600)             
            # Recursive function to iterate the files
            changePermissionsRecursively(itempath, uid, gid)

def getConfigPath(configFileName = None):
    """
        Auxiliar function to get the configuration path depending on the system.
    """
    if configFileName != None:
        # Returning the path of the configuration file
        if sys.platform == 'win32':
            return os.path.expanduser(os.path.join('~\\', 'Deepify', configFileName))
        else:
            return os.path.expanduser(os.path.join('~/', '.config', 'Deepify', configFileName))
    else:
        # Returning the path of the configuration folder
        if sys.platform == 'win32':
            return os.path.expanduser(os.path.join('~\\', 'Deepify'))
        else:
            return os.path.expanduser(os.path.join('~/', '.config', 'Deepify'))

def getConfiguration(configPath = None):
    """
        Reading the configuration file to look for where the different gates are running.
        
        :return: A json containing the information stored in the .cfg file.
    """
    if configPath == None:
        # If a current.cfg has not been found, creating it by copying from default
        configPath = getConfigPath("browser.cfg")

    # Checking if the configuration file exists
    if not os.path.exists(configPath):
        try:
            # Copy the data from the default folder
            defaultConfigPath = getConfigPath(os.path.join("default", "browser.cfg"))
     
            with open(configPath, "w") as oF:
                with open(defaultConfigPath) as iF:
                    cont = iF.read()
                    oF.write(cont)    
                                                
        except Exception, e:
            errMsg = "ERROR. No configuration file could be found and the default file was not found either. You might need to reset it manually."
            raise Exception( errMsg + " " + str(e))      

    try:
        # Reading the configuration file
        config = ConfigParser.ConfigParser()
        config.read(configPath)

        info = {}

        # Iterating through all the sections, which contain the platforms
        for section in config.sections():
            current = {}
            # Iterating through parametgers
            for (param, value) in config.items(section):
                current[param] = value
                
            # Loading the configuration in the info dictionary
            info[section] = current
            
    except Exception, e:
        errMsg = "ERROR. Something happened when processing the Configuration file (some kind of malform?). Check it before running it again."
        raise Exception( errMsg + " " + str(e))      

    return info

