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

import deepify.utils.configuration as configuration
import datetime as dt
import json
import re

class Wrapper():
    """
        <Wrapper> class.
    """
    def __init__(self):
        """
            Constructor without parameters...
        """
        # As would be defined in the browser.cfg
        self.name = "Wrapper"
        self.domainRegexp = "https?://([a-zA-Z0-9]+\.[^\/]+)/.*"
        # Letting it as default
        self.info = {}
        
    def _getConfiguration(self):
        """
            Method that abstracts the extraction of grabbing the configuration.
            
            :return: the applicable configuration settings.
        """
        info =configuration.getConfiguration()

        try:            
            # This returns only the parameters needed by each wrapper. E. g., for Tor:
            # {
            #    "host" : "127.0.0.1"
            #    "port" : "9150"
            # }    
            return info[self.name]
            
        except KeyError, e:
            errMsg = "ERROR. WTF! There was not found any configuration for " + self.name + " in the configuration file!"
            raise Exception( errMsg )
            
    def getDomainFromUrl(self, url):
        """
            Extracting the domain from the URL.
            
            :return: domain as a string.
        """
        try:
            domain = re.findall( self.domainRegexp, url )[0]
        except Exception, e:
            errMsg = "ERROR. Something happened when trying to find the domain from <" + url + ">. Are you sure that the following regular expression matches a domain in the url provided?\n\t" + self.domainRegexp
            raise Exception( errMsg + "\n" + str(e) )
                    
        return domain

    def _rebuildHTMLContent(self, linesArray):
        """ 
            Grabbing a list of lines and rebuilding the HTML as a string.
            
            :return aux: The HTML string.
        """
        aux = ""
        for l in linesArray:
            aux+= l +"\n"
        return aux

    def _createDataStructure(self, content):
        """
            This method receives a response, including headers, and creates the appropriate structure.
            :param url: The URL to be recovered.
            :param content: The content of the response.                
            
            :return: A json.        
        """
        aux = {}
        aux["headers"] = {}
        aux["content"] = ""
        for i, line in enumerate(content.splitlines()):
            if i == 0:
                aux["procotol"] = line.split()[0]
                aux["code"] = line.split()[1]
            elif line != "":
                header =  line.split(": ")[0]
                aux["headers"][header] = line[line.find(": ")+2:]
            else:
                aux["content"] += self._rebuildHTMLContent(content.splitlines()[i+1:])
                
                # TO-DO: Perform additional processing of the HTML
                
                break  
        return aux

    def _grabContentFromUrl(self, url):
        """ 
            Function that abstracts capturing a URL. This method will be rewritten in child classes.
            
            :param url: The URL to be processed.
            :return:    The response in a Json format.
        """
        # Defining an empty object for the response
        response = {}

        # This part has to be modified...        
        try:
            import urllib2

            # Grabbing the data      
            data = urllib2.urlopen(url).read()

            # Processing the data as expectesd
            response = self._createDataStructure(data)        
            
        # Try to make the errors clear for other users
        except Exception, e:
            errMsg = "ERROR. Something happened."   
            raise Exception( errMsg + " " + str(e))
            
        return response        

    def getResponse(self, url):
        """ 
            Public method that wraps the extraction of the content.
            
            :param url: The resource to be processed.
            :return:    The response in a Json format.
        """     
        # Defining an empty object for the response
        response = {}
        try:
            # This receives only the parameters needed by this Tor Wrapper:
            # {
            #    "host" : "127.0.0.1"
            #    "port" : "9150"
            # }  
            self.info = self._getConfiguration()
        
            response = self._grabContentFromUrl(url)
        except Exception, e:
            response["status"] = { "code" : 400, "desc" : str(e) }            
            
        # Adding other known data            
        response["time_processed"] = str(dt.datetime.now())
        
        response["domain"] = self.getDomainFromUrl(url)
        response["url"] = url          

        try:
            # We'll check if something happened...    
            response["status"]
        except Exception, e:
            # If nothing happened till now, we'll set the code as 200             
            response["status"] = { "code" : 200, "desc" : "OK." }
                    
        return response                  
