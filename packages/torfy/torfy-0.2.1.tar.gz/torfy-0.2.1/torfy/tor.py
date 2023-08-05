#!/usr/bin/env python
# -*- coding: cp1252 -*-
#
##################################################################################
#
#    Copyright 2016 Félix Brezo and Yaiza Rubio (i3visio, contacto@i3visio.com)
#
#    This file is part of Torfy. You can redistribute it and/or modify
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
import socket
import socks
from torfy.utils.wrapper import Wrapper

class Tor(Wrapper):
    """
        A <Wrapper> class that defines the the special processing that Tor needs.
        
        Inherited functions:
            -     def _getConfiguration(self):
            -     def _getDomainFromUrl(self, url):
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
        self.name = "Tor Browser"
        self.domainRegexp = "https?://([a-zA-Z0-9]+\.onion)/.*"
        # Letting it as default
        self.info = {}
        
    def _grabContentFromUrl(self, url):
        """ 
            Function that abstracts capturing a URL. This method rewrites the one from Wrapper.
            
            :param url: The URL to be processed.
            :return:    The response in a Json format.
        """
        # Defining an empty object for the response
        response = {}
                
        # This part has to be modified...        
        try:            
            # Configuring the socket
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, self.info["host"], int(self.info["port"]), True)
            s = socks.socksocket()
            
            # Extracting the domain from the URL
            domain = self._getDomainFromUrl(url)        
            s.connect((domain, 80))

            message = 'GET ' + url + ' HTTP/1.0\r\n\r\n'
            s.sendall(message)
            
            data = ""
            while True:
                reply = s.recv(4096)

                if not reply:
                    break    
                else:
                    data += reply    
            
            # Processing data as expected
            response = self._createDataStructure(data)     
            
        # Try to make the errors clear for other users
        except socks.ProxyConnectionError, sPCE:
            errMsg = "ERROR socks.ProxyConnectionError. Something seems to be wrong with the Tor Bundler."   
            raise Exception( errMsg + " " + str(sPCE))        
            
        return response   
