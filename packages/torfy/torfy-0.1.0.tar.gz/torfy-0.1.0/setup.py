# !/usr/bin/python
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

import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))

# Importing the local scrips for the setup and taking the new version number
import torfy
NEW_VERSION = torfy.__version__

import torfy.configuration as configuration

# Depending on the place in which the project is going to be upgraded
from setuptools import setup
try:
    raise Exception('Trying to load the markdown manually!')    
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()
except Exception:
    read_md = lambda f: open(f, 'r').read()

# Reading the .md file    
try:
    long_description = read_md(os.path.join(HERE,"README.md"))
except:
    long_description = ""


# Creating the application path
applicationPath = configuration.getConfigPath()
applicationPathDefaults = os.path.join(applicationPath, "default")

# Copying the default configuration files.
if not os.path.exists(applicationPathDefaults):
    os.makedirs(applicationPathDefaults) 
	
# Launching the setup
setup(    name="torfy",
    version=NEW_VERSION,
    description="Torfy - A set of GPLv3+ libraries to deal with Tor connections.",
    author="Felix Brezo and Yaiza Rubio",
    author_email="contacto@i3visio.com",
    url="http://github.com/i3visio/torfy",
    license="COPYING",
    keywords = "python osint harvesting networking tor privacy",
    scripts= [
        "scripts/onionGet.py",            
        "scripts/onionsFromFile.py",            
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)', 
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',   
        'Intended Audience :: Information Technology',      
        'Intended Audience :: Science/Research',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'Topic :: Communications',   
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',  
        'Topic :: Text Processing :: Markup :: HTML'                                 
    ],    
    packages=[
        "torfy", 
    ],
    long_description=long_description,
    install_requires=[
        "argparse",
        "pysocks",
    ],    
)

############################
### Creating other files ###
############################
try:
    configuration.changePermissionsRecursively(applicationPath, int(os.getenv('SUDO_UID')), int(os.getenv('SUDO_GID')))              
except:
    # Something happened with the permissions... We omit this.
    pass

files_to_copy= {
    applicationPath : [
    ],
    applicationPathDefaults : [
        os.path.join("config", "browser.cfg"),
    ]
}

# Iterating through all destinations to write the info
for destiny in files_to_copy.keys():
    # Grabbing each source file to be moved
    for sourceFile in files_to_copy[destiny]:
        fileToMove = os.path.join(HERE,sourceFile)

        # Choosing the command depending on the SO
        if sys.platform == 'win32':
            cmd = "copy \"" + fileToMove + "\" \"" + destiny + "\""
        elif sys.platform == 'linux2' or sys.platform == 'darwin':   
            cmd = "sudo cp \"" + fileToMove + "\" \"" + destiny + "\""
        #print cmd
        output = os.popen(cmd).read()    

print    
