# import os
import datetime
# import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
# from requests import HTTPError

if __name__ == '__main__':
    from assignment import Assignment
else:
    from staxing.assignment import Assignment


class StaxHelper(object):
    ''''''
    LOCAL = False  # use ChromeDriver locally
    REMOTE = not LOCAL  # use Sauce Labs
    CONDENSED_WIDTH = 767  # pixels
    WAIT_TIME = Assignment.WAIT_TIME  # seconds
