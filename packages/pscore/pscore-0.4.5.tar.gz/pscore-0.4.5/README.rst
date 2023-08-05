======
PSCORE
======

``pscore`` provides a range of selenium webdrivers for local, grid and saucelabs execution, including test setup and teardown. It has been tested and used with the ``nose2`` test runner which enables multi-threaded test execution. ``pscore`` offers up a ``WebDriverTestCase`` which can be sub-classed in your automation test cases and will provide access to a ``webdriver`` object via ``self.driver``

An example test looks like this::

    from pscore.core.wd_testcase import WebDriverTestCase
    from pscore.nose2.tags import tagger
    from the_internet_model.pages.home import Home

    class TestTheInternet(WebDriverTestCase):

    @tagger('Home')
     def test_can_load_homepage(self):
         home = Home(self.driver).load()
         self.assertTrue(home.is_loaded(), "Error loading homepage")

And is run like this::

    nose2 -c nose2.cfg -A tags=Home

Test configuration is managed by reading environment variables.

""""""""""""""""""""""""""""""
Required environment variables
""""""""""""""""""""""""""""""

* ``PSCORE_ENVIRONMENT`` - Specifies the execution environment.  Accepted values: `grid`, `local`, `saucelabs`, `sauce`, `amazon`
* ``PSCORE_BROWSER`` - Specifies the browser.  Accepted values: `ie`, `chrome`, `firefox`, `iphone`, `ipad`, `android`, `safari` (`ie`, `chrome`, `firefox`, `android` options can be used on local development)
* ``PSCORE_HOMEPAGE`` - Specifies the homepage.  e.g. http://www.google.com

Others
""""""

* ``PSCORE_BROWSER_VERSION`` (e.g. if using saucelabs) - specify browser version
* ``PSCORE_SCREENSHOT_DIR`` - Specifies the directory to write screenshots to
* ``PSCORE_AGENT_ID``- (optional) name to set the ``environment`` of your test run e.g. ``"MyTeamIntReview"``
* ``PSCORE_SELENIUM_HUB_URL`` - Specifies the URL of a standard selenium hub instance e.g. ``http://gridhub:4444/wd/hub``
* ``PSCORE_HTML_DUMP_ON_FAILURE`` - when ``True``, a failing test will add page source to log files during teardown.

Saucelabs
"""""""""

* ``PSCORE_SAUCE_USERNAME`` - The username to use for Saucelabs authentication
* ``PSCORE_SAUCE_KEY`` - The access key to use for Saucelabs authentication
* ``PSCORE_SAUCE_TUNNEL_ID`` - in order to see internal test environments, we need to use a sauce connect tunnel - use the tunnel ID name
* ``PSCORE_SAUCE_PARENT_ACCOUNT`` - if you are a sub-account of someone else, put that username here

"""""""""""""""""
Driver Extensions
"""""""""""""""""

``pscore`` offers some extensions to the webdriver API

Waiting
"""""""

There are some wait helpers::

    a_findable_element = By.XPATH, "//div[@id='start']/button"
    some_spinner = By.ID, "alert_spinner"
    how_long_to_wait = 10 #seconds
    # We can wait until something appears
    element_found = self.driver.wait.until_visible2(a_findable_element, how_long_to_wait)
    # or wait until something has gone away
    element_gone = self.driver.wait.until_not_visible2(some_spinner, how_long_to_wait)
    # Exceptions are suppressed so these methods always return true or false


"""""""""""""""""""""""""
Using Custom Capabilities
"""""""""""""""""""""""""

Usually, we would suggest using the environment variables above for test configuration. There will be times when you may want to use custom capabilities.
Here is an example of how you can do that. We still set the ``PSCORE_ENVIRONMENT`` to either `sauce`, `local` or `grid`. ::

    caps = dict(
        browserName='chrome',
        platform='Windows 8',
        version='47.0',
        screenResolution='1280x1024'
    )


    class SimpleSauceCapsTest(WebDriverTestCase):
        def setUp(self):
            # You must assign custom_caps
            self.custom_caps = caps
            # Then call super
            super(SimpleSauceCapsTest, self).setUp()

        @tagger('dbg')
        def test_customCaps(self):
            self.driver.get("http://www.google.com")
            self.assertTrue(False)

