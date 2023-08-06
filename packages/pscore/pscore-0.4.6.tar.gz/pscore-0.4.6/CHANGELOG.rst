"""""""""""""""
Release History
"""""""""""""""

0.4.6 (2016-04-11)
""""""""""""""""""

* Fixed a bug in pscore which was failing to upload logs to reporting service when using params

0.4.5 (2016-03-14)
""""""""""""""""""

* Added Applitools support for use with Saucelabs

0.4.4 (2016-02-26)
""""""""""""""""""

* Selenium 2.52.0 bindings
* Make test fail and teardown gracefully if an uncaught exception is thrown from an overridden ``tearDown`` implementation
* Prevent setup logic from attempting to maximise window when using custom mobile capabilities

0.4.3 (2016-02-05)
""""""""""""""""""

* Support for Custom Desired Capabilities (see examples above)
* New flag ``PSCORE_HTML_DUMP_ON_FAILURE`` will place ``driver.page_source`` into log file if a test fails.

0.4.2 (2016-01-29)
""""""""""""""""""

* Sanitize log file names when running `parameterized tests <http://nose2.readthedocs.org/en/latest/plugins/parameters.html>`_.
* Selenium 2.50.0 bindings


0.4.1 (2016-01-22)
""""""""""""""""""

* Sauce Android caps updated to support 5.1

0.4.0 (2016-01-21)
""""""""""""""""""

* Compatible with Python 3.5.*
* Update Selenium version to 2.49.2
* Fixed an issue where a logger instantiation error caused tests not to execute
* Teardown URL logged for all ``PSCORE_ENVIRONMENT`` s

0.3.4 (2015-12-22)
""""""""""""""""""

* Update Selenium version to 2.48.0
* Added ``driver.wait.until_visible2`` and ``driver.wait.until_not_visible2``. Example usage above

0.3.3 (2015-12-10)
""""""""""""""""""

Fix for displaying sauce reports when there is a timeout on sauce side

0.3.2 (2015-11-02)
""""""""""""""""""

Updated Sauce caps to use the latest keys and added support for safari 9

0.3.1 (2015-10-20)
""""""""""""""""""

Minor fix for handling exceptions when artefact service was down

0.3.0 (2015-10-02)
""""""""""""""""""

Bumped the selenium version to use 2.47.3

0.2.4 (2015-09-25)
""""""""""""""""""

Added the capability to log the grid node ip

0.2.3 (2015-09-25)
""""""""""""""""""

Fixed the bug which was not downloading the chromedriver and iedriver when trying to run the tests locally

0.2.2 (2015-09-24)
""""""""""""""""""

Missing changelog file was causing ``setup.py`` to crash

0.2.1.1 (2015-09-24)
""""""""""""""""""""

Minor fixes in the way error messages are captured