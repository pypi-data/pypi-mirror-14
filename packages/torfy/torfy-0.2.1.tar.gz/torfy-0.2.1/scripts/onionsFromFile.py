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

'''
onionsFromFile.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2016
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
For details, run:
    python onionsFromFile.py --license
'''
__author__ = "Felix Brezo, Yaiza Rubio "
__copyright__ = "Copyright 2016, i3visio"
__credits__ = ["Felix Brezo", "Yaiza Rubio"]
__license__ = "GPLv3+"
__version__ = "v0.2.0"
__maintainer__ = "Felix Brezo, Yaiza Rubio"
__email__ = "contacto@i3visio.com"

import argparse
import os
import json
import torfy.utils.banner as banner
from torfy.tor import Tor
import datetime as dt
from multiprocessing import Pool


def multi_run_wrapper(params):
    '''
        Wrapper for being able to launch all the threads.
        :param params: We receive the parameters as a tuple.
    '''
    onion, index, total = params
    print "[" + str(index) + "/" + str(total) + "] ", dt.datetime.now(), ":\tRecovering information from ", onion
    # Reading content
    torWrapper = Tor()
    response = torWrapper.getResponse(onion)

    if response["status"]["code"] != 200:
        print dt.datetime.now(), ":\tSomething happened when launching the query for <" + onion +">.\nError message: " + response["status"]["desc"]

    print "[" + str(index) + "/" + str(total) + "] ", dt.datetime.now(), ":\tStoring information from", onion
    # Storing the full processed response
    with open(os.path.join(args.output_folder, response["domain"] +".json"), "w") as oF:
        try:
            oF.write(json.dumps(response, indent = 2))
        except Exception, e:
            # Grabbing possible exceptions that may occur when using json library...
            oF.write(response)                

    with open(os.path.join(args.output_folder, response["domain"] +".html"), "w") as oF:                        
        try:            
            # Storing only the HTML
            oF.write(response["content"])
        except Exception, e:
            # Probably... no content found.
            oF.write("")                
            pass 


def main(args):
    """
        Main function
    """
    urls = []
    
    # Grabbing all possible URL
    with open(args.file) as iF:
        urls = iF.read().splitlines()

    # Creating the output folder if it does not exist.
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Using threads in a pool if we are not running the program in main
    onions = []

    for i, url in enumerate(urls):
        onions.append((url, i+1, len(urls)))     

    # If the process is executed by the current app, we use the Processes. It is faster than pools.
    if args.threads <= 0 or args.threads > len(onions):
        nThreads = len(onions)
    else:
        nThreads = args.threads
        
    # Launching the Pool
    # ------------------
    #logger.info("Launching " + str(nThreads) + " different threads...")
    # We define the pool
    pool = Pool(nThreads)

    # We call the wrapping function with all the args previously generated
    poolResults = pool.map(multi_run_wrapper,onions)

    pool.close()                     


def getParser():
    parser = argparse.ArgumentParser(description='onionsFromFile.py - Grabbing Tor URLs from a file.', prog='onionsFromFile.py', epilog='Check the README.md file for further details on the usage of this program or follow us on Twitter in <http://twitter.com/i3visio>.', add_help=False)
    parser._optionals.title = "Input options (one required)"

    # Defining the mutually exclusive group for the main options
    groupMainOptions = parser.add_mutually_exclusive_group(required=True)
    # Adding the main options
    groupMainOptions.add_argument('--license', required=False, action='store_true', default=False, help='shows the GPLv3+ license and exists.')
    groupMainOptions.add_argument('-f', '--file', metavar='<path>', action='store', help = 'path to the file (one URL per line).')

    # Configuring the processing options
    groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the way in which torfy will process the URL.')
    groupProcessing.add_argument('-o', '--output_folder', metavar='<path_to_output_folder>', required=False, default = './results', action='store', help='output folder for the generated documents. While if the paths does not exist, usufy.py will try to create; if this argument is not provided, usufy will NOT write any down any data. Check permissions if something goes wrong.')
    groupProcessing.add_argument('-t', '--threads', metavar='<num_threads>', required=False, action='store', default=16, type=int, help='write down the number of threads to be used (default 16). If 0, the maximum number possible will be used, which may make the system feel unstable.')        

    # About options
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    groupAbout.add_argument('--version', action='version', version='%(prog)s ' +__version__, help='shows the version of the program and exists.')

    return parser

if __name__ == "__main__":
    print banner.WELCOME_TEXT
    
    # Grabbing the parser
    parser = getParser()

    args = parser.parse_args()

    # Calling the main function
    main(args)   
