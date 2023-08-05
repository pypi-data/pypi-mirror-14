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

import configuration
import datetime as dt
import json
import os
import re
import socket
import socks
import sys


def getDomainFromUrl(url):
    """
        Extracting the .onion domain from a URL.
        
        :return: domain as a string.
    """
    domain = re.findall("https?://([a-zA-Z0-9]+\.onion)/.*", url)[0]
    return domain

def rebuildHTMLContent(linesArray):
    """ 
        Grabbing a list of lines and rebuilding the HTML as a string.
        
        :return aux: The HTML string.
    """
    aux = ""
    for l in linesArray:
        aux+= l +"\n"
    return aux

def createDataStructure(content):
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
            aux["content"] += rebuildHTMLContent(content.splitlines()[i+1:])
            break  
    return aux

        
def grabOnionUrl(url):
    """ 
        Function that abstracts capturing an onion URL.
        :param url: The Tor URL to be processed.
        :return:    The HTML content.
    """
    # Configuring default proxy
    try:
        # Grabbing the configuration options from default.        
        info = configuration.getConfiguration()
        
        # Configuring the socket
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, info["host"], int(info["port"]), True)
        s = socks.socksocket()
        
        # Extracting the domain from the URL
        domain = getDomainFromUrl(url)        
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
        
        # Processing data
        response = createDataStructure(data)

        response["time"] = str(dt.datetime.now())
        response["domain"] = domain

        # TO-DO: Perform additional processing here

        return response
        
    except socks.ProxyConnectionError, sPCE:
        print "ERROR socks.ProxyConnectionError: Something seems to be wrong with the Tor Bundler."
        print str(sPCE)    
        sys.exit()

def test():
    print "test"
