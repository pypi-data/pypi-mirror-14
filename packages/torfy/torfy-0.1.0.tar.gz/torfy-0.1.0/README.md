Torfy
=====

Copyright (C) 2016  F. Brezo and Y. Rubio, i3visio

[![Version in PyPI](https://img.shields.io/pypi/v/torfy.svg)]()
[![Downloads/Month in PyPI](https://img.shields.io/pypi/dm/torfy.svg)]()
[![License](https://img.shields.io/badge/license-GNU%20General%20Public%20License%20Version%203%20or%20Later-blue.svg)]()

1 - Description
---------------

OSRFramework is a GPLv3+ set of libraries developed by i3visio to perform Open Source Intelligence tasks. They include references to a bunch of different applications related to username checking, information leaks research, deep web search, regular expressions extraction and many others. At the same time, by means of ad-hoc Maltego transforms, OSRFramework provides a way of making these queries graphically.


2 - License: GPLv3+
-------------------

This is free software, and you are welcome to redistribute it under certain conditions.

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.


For more details on this issue, check the [COPYING](COPYING) file.

3 - Installation
----------------

Fast way to do it on any system:
```
pip install torfy
```
Under MacOS or Linux systems, you may need to do this as superuser:
```
sudo pip install torfy
```
This will manage all the dependencies for you.

If you needed further information, check the [INSTALL.md](INSTALL.md) file.

4 - Basic usage
---------------

If everything went correctly (we hope so!), it's time for trying torfy.py. But first, you will need to start the Tor Bundle downloadable from `http://torproject.org`. Execution examples:
```
onionGet.py -u "http://3g2upl4pq6kufc4m.onion/"
```

Type -h or --help to get more information about which are the parameters of the application.

You can also use the functions as a library:
```
import torfy.torwrapper as torwrapper
url = "http://3g2upl4pq6kufc4m.onion/"
data = torwrapper.grabOnionUrl(url)
print data
```

5 - HACKING
-----------

If you want to extend the functionalities of Torfy and you do not know where to start from, check the [HACKING.md](HACKING.md) file.

6 - AUTHORS
-----------

More details about the authors in the [AUTHORS.md](AUTHORS.md) file.
