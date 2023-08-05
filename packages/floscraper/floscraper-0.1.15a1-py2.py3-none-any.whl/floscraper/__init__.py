# -*- coding: UTF-8 -*-
"""
An scraper utility package
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2014-16, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.15a1"
__date__ = "2016-03-08"

import logging

from .webscraper import WebScraper, default_user_agents, \
    WEBConnectException, WEBFileException, WEBParameterException


logger = logging.getLogger(__name__)
__all__ = ["webscraper"]
