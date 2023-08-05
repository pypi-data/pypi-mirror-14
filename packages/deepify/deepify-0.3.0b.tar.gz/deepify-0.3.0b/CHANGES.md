Deepify Changelog
=================

For more information, check the README.md in <http://github.com/i3visio/deepify>.

0.3.0, 2016/03/14 -- Changed the name of the library and other minor fixes.
- All references to torfy has been changed to deepify, as this is a more general approach.
- Change in the getDomainFromUrl which now is a public function. 

0.2.2, 2016/03/07 -- Fixed an issue when launching onionsFromFile.py.
- There was an issue when launching the onionsFromFile.py as some variables where impossible to be caught.

0.2.1, 2016/03/06 -- Added threading to onionsFromFile.py.
- Adding threading options to the file to fasten the process of getting tor connections.
- The HTML code is now stored in onionsFromFile and exceptions are managed better.

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

