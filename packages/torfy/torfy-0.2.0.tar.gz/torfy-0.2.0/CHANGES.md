Torfy Changelog
===============

For more information, check the README.md in <http://github.com/i3visio/torfy>.

0.2.0, 2016/03/04 -- Abstraction of the classes.
- Abstracting the conception of the wrappers to make it easy further improvements. Class inheritance has been included.
- Refactorization of the torfy folder.
- Added two new fields to the response: "status" (a new dictionary that maps the status of the response) and "url". "time" has also been moved to "time_processed".

0.1.0, 2016/03/01 -- Initial release.
- Added conectivity to a running instance of Tor Browser.
- Added configuration files with connection details.
- Added preprocessing of the response grabbed from the Tor Browser: domain, timestamp, headers, HTTP response and content are processed.
- Added two scripts that can be launched via the terminal: onionGet.py and onionsFromFile.py.
- Added basic documentation documents.
- Creation of the main modules.

