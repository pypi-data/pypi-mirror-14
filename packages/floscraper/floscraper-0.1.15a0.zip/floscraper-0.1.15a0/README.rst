FLOSCRAPER
##########

Some basic webscraper I use in many projects.

.. image:: https://img.shields.io/pypi/v/floscraper.svg
    :target: https://pypi.python.org/pypi/floscraper

.. image:: https://img.shields.io/pypi/l/floscraper.svg
    :target: https://pypi.python.org/pypi/floscraper

.. image:: https://img.shields.io/pypi/dm/floscraper.svg
    :target: https://pypi.python.org/pypi/floscraper


webscraper
==========
Module to ease web efforts

**Supports**

* Cached web requests (Wrapper around requests)
* Bultin parsing/scraping (Wrapper around beautifulsoup)


**Constructor parameters**

* url: Default url, used if nothing else specified
* scheme: Default scheme for scrapping
* timeout
* cache_directory: Where to save cache files
* cache_time: How long is a cached resource vaild - in seconds (default: 7 minutes)
* cache_use_advanced
* auth_method: Authentication method (default: HTTPBasicAuth)
* auth_username: Authentication username. If set, enables authentication
* auth_password: Authentication password
* handle_redirect: Allow redirects (default: True)
* user_agent: User agent to use
* default_user_agents_browser: Browser to set in user agent (from ``default_user_agents`` dict)
* default_user_agents_os: Operating system to set in user agent (from ``default_user_agents`` dict)
* user_agents_browser: Browser to set in user agent (Overwrites default_user_agents_browser)
* user_agents_os: Operating system to set in user agent (Overwrites default_user_agents_os)
* html2text: HTML2text settings
* html_parser: What html parser to use (default: html.parser - built in)


**Example**

.. code-block:: python

    # Setup WebScraper with caching
    web = WebScraper({
        'cache_directory': "cache",
        'cache_time': 5*60
    })
    
    # First call to git -> hit internet
    web.get("https://github.com/")
    
    # Second call to git (within 5 minutes of first) -> hit cache
    web.get("https://github.com/")

Whitch results in the following output:

::

    2016-01-07 19:22:00 DEBUG   [WebScraper._getCached] From inet https://github.com
    2016-01-07 19:22:00 INFO    [requests.packages.urllib3.connectionpool] Starting new HTTPS connection (1): github.com
    2016-01-07 19:22:01 DEBUG   [requests.packages.urllib3.connectionpool] "GET / HTTP/1.1" 200 None
    2016-01-07 19:22:01 DEBUG   [WebScraper._getCached] From cache https://github.com
