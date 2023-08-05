#!/usr/bin/env python
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

import datetime as dt
import urllib2
from deepify.utils.wrapper import Wrapper

class Zeronet(Wrapper):
    """
        A <Wrapper> class that defines the the special processing that Zeronet needs.
        
        Inherited functions:
            -     def _getConfiguration(self):
            -     def getDomainFromUrl(self, url):
            -     def _rebuildHTMLContent(self, linesArray):
            -     def getResponse(self, url):            

        Rewritten functions:
            -     def _grabContentFromUrl(self, url):                    
            -     def __init__(self, content):          
    """
    
    def __init__(self):
        """
            Constructor without parameters...
        """
        # As would be defined in the browser.cfg
        self.name = "Zeronet"
        self.domainRegexp = "(.+)"
        # Letting it as default
        self.info = {}
        
    def _grabContentFromUrl(self, url):
        """ 
            Function that abstracts capturing a URL. This method rewrites the one from Wrapper.
            
            :param url: The URL to be processed.
            :return:    The response in a Json format.
        """
        # Defining an empty object for the response
        info = {}
                
        # This part has to be modified...        
        try:            
            # Configuring the socket
            queryURL = "http://" + self.info["host"] + ":" + self.info["port"] + "/" + url
            response = urllib2.urlopen(queryURL)

            # Rebuilding data to be processed
            data = str(response.headers) + "\n"

            data += response.read()

            # Processing data as expected
            info = self._createDataStructure(data)     
            
        # Try to make the errors clear for other users
        except Exception, e:
            errMsg = "ERROR Exception. Something seems to be wrong with the Zeronet Bundler."   
            raise Exception( errMsg + " " + str(e))        
            
        return info   
        
