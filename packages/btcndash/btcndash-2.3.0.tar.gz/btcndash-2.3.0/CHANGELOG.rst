Changes
=======

v2.3.0, April 3, 2016

* Documentation updates
* Allow name of node to be customized
* Make location variables accessible to templates directly
* Move formatting into the templates themselves
* Fixed some Python 2/3 issues
* New tiles: bitnodes data and fee summary
* Always load default config first, then overwrite with any custom config

v2.2.0, March 26, 2016

* Added interactive tables to the transactions and peers pages
* Added several new tiles and reformatted others. Made the new ones the default, but originals
  are still present if desired.
* Some code cleanup and fixes
* Allow an argument to RPC commands
* Make some logging less verbose
* Documentation updates

v2.1.0, March 20, 2016

* Return config file to plain text, this time json
* Add command line options:

  * Specify location of config file
  * Clear page cache on startup

* Update js libraries (Highcharts and jQuery)
* Add config options to add additional locations for views and static files
* Add a setup.py file and publish to PyPI
* Updated documentation and use Sphinx to make it pretty

v2.0.0, March 16, 2016

* Significant refactoring under the hood
* Allow reordering, disabling and adding custom tiles
* Config file now python to allow more powerful customization
* Preliminary support for Python 3.5
* Remove CherryPy as a dependency (default to wsgiref instead)
* Add config variable for header title
* Bug fixes

v1.0.1, March 8, 2016

* Fixed a bug with float data type

v1.0.0, March 8, 2016

* Bumped version to 1.0

v0.1.1, Jan 1, 2015

* Added a more graceful failure when the Bitcoin node is not reachable
* Clarified Python version requirements
* Bumped versions of dependencies

v0.1.0, May 25, 2014

* Initial release.
