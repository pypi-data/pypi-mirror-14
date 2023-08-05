"""OpenStax Python helper for common actions."""

import datetime
import inspect
import os
import sys
import unittest

from builtins import FileNotFoundError
from requests import HTTPError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from urllib.parse import urlparse, ParseResult

try:
    from staxing.assignment import Assignment
except ImportError:
    from assignment import Assignment


class StaxHelper(object):
    """Primary OpenStax control class."""

    CONDENSED_WIDTH = 767  # pixels
    DEFAULT_WAIT_TIME = 15  # seconds

    def __init__(self, driver_type='chrome', capabilities=None,
                 pasta_user=None, wait_time=DEFAULT_WAIT_TIME,
                 opera_driver='/Applications/operadriver', initial_user=None):
        """Class initialize."""
        self.webdriver_service = None
        self.user = initial_user
        if driver_type == 'saucelabs' and pasta_user is None:
            raise TypeError('A Sauce Labs user is required for remote testing')
        self.pasta = pasta_user
        self.driver = self.run_on(driver_type, self.pasta, capabilities)
        self.driver.implicitly_wait(wait_time)

    def run_on(self, driver_type, pasta_user, capabilities=None,
               wait=DEFAULT_WAIT_TIME, opera_driver=''):
        """Webdriver activation.

        driver_type (string): web browser type
        pasta_user (PastaSauce): optional API access for saucelabs
        capabilities (dict): browser settings; copy object to avoid overwrite
            Defaults:
                DesiredCapabilities.ANDROID.copy()
                DesiredCapabilities.CHROME.copy()
                DesiredCapabilities.EDGE.copy()
                DesiredCapabilities.FIREFOX.copy()
                DesiredCapabilities.HTMLUNIT.copy()
                DesiredCapabilities.HTMLUNITWITHJS.copy()
                DesiredCapabilities.INTERNETEXPLORER.copy()
                DesiredCapabilities.IPAD.copy()
                DesiredCapabilities.IPHONE.copy()
                DesiredCapabilities.ORERA.copy()
                DesiredCapabilities.PHANTOMJS.copy()
                DesiredCapabilities.SAFARI.copy()
            Keys:
                platform
                browserName
                version
                javascriptEnabled
        wait (int): standard time, in seconds, to wait for Selenium commands
        opera_driver (string): Chromium location
        """
        try:
            return {
                'firefox': lambda: webdriver.Firefox(),
                'chrome': lambda: webdriver.Chrome(),
                'ie': lambda: webdriver.Ie(),
                'opera': lambda: self.start_opera(opera_driver),
                'phantomjs': lambda: webdriver.PhantomJS(),
                'saucelabs': lambda: webdriver.Remote(
                    command_executor=(
                        'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
                        (pasta_user.get_user(), pasta_user.get_access_key())
                    ),
                    desired_capabilities=capabilities
                ),
            }[driver_type]()
        except WebDriverException as err:
            raise FileNotFoundError(err)
        except Exception as err:
            raise self.WebDriverTypeException(
                msg='Unknown WebDriver type: "%s"' % driver_type,
                err=err.__traceback__
            )

    def start_opera(self, location):
        """Opera initiator."""
        from selenium.webdriver.chrome import service
        webdriver_service = service.Service(location)
        webdriver_service.start()
        return webdriver.Remote(
            webdriver_service.service_url,
            webdriver.DesiredCapabilities.OPERA
        )

    @classmethod
    def date_string(cls, day_delta=0, str_format='%m/%d/%Y'):
        """System date format for Tutor."""
        return (datetime.date.today() + datetime.timedelta(days=day_delta)). \
            strftime(str_format)

    def quit(self):
        """Attempt to cleanly close down the WebDriver."""
        try:
            self.driver.quit()
        except:
            pass

    def get(self, url):
        """Return the current URL."""
        self.driver.get(url)

    def get_window_size(self, dimension=None):
        """Return the current window dimensions."""
        get_size = self.driver.get_window_size()
        if dimension is None:
            return get_size
        if dimension not in get_size:
            raise IndexError('Unknown dimension: %s' % dimension)
        return get_size[dimension]

    def sleep(self, seconds=1):
        """Stop execution for the specified time in seconds."""
        sleep(seconds)


class WebDriverTypeException(WebDriverException):
    """Exception for unknown WebDriver types."""

    def __init__(self, msg, err):
        """Exception initializer."""
        self.msg = msg
        self.__traceback__ = err

    def __str__(self):
        """String representation of the exception."""
        return repr(self.msg, self.__traceback__)


class User(object):
    """User parent class."""

    DEFAULT_WAIT_TIME = StaxHelper.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 email_username=None, email_password=None):
        """Base case initialization."""
        self.username = username
        self.password = password
        parse = list(urlparse(site if urlparse(site).scheme else
                     '%s%s' % ('//', site)))
        parse[0] = b'https'
        for index, value in enumerate(parse):
            parse[index] = value.decode('utf-8') if isinstance(value, bytes) \
                else value
        parse = ParseResult(*parse)
        self.url = parse.geturl()
        self.email = email
        self.email_username = email_username
        self.email_password = email_password

    def login(self, driver, username=None, password=None, url=None,
              wait_time=DEFAULT_WAIT_TIME):
        """
        Tutor login control.

        Requires a Tutor or Accounts instance
        Branching to deal with standard or compact screen widths

        driver (WebDriver): active driver connection
        username (string): website username
        password (string): website password
        url (string): website URL
        wait_time (int): Selenium default wait time, in seconds
        """
        wait = WebDriverWait(driver, wait_time)
        url_address = self.url if url is None else url
        # open the URL
        driver.get(url_address)
        if 'tutor' in url_address:
            # check to see if the screen width is normal or condensed
            if driver.get_window_size()['width'] <= \
                    StaxHelper.CONDENSED_WIDTH:
                # get small-window menu toggle
                is_collapsed = driver.find_element(
                    By.XPATH,
                    '//button[contains(@class,"navbar-toggle")]'
                )
                # check if the menu is collapsed and, if yes, open it
                if('collapsed' in is_collapsed.get_attribute('class')):
                    is_collapsed.click()
            driver.find_element(By.LINK_TEXT, 'Login').click()
        wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//html/body')
            )
        )
        import re
        src = driver.page_source
        text_located = re.search(r'openstax', src.lower()) is not None
        if not text_located:
            raise self.LoginError('Non-OpenStax URL: %s' %
                                  driver.current_url)
        # enter the username and password
        driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.username if username is None else username)
        driver.find_element(By.ID, 'password'). \
            send_keys(self.password if password is None else password)
        # click on the sign in button
        driver.find_element(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()

    def logout(self, driver):
        """Logout control."""
        url_address = driver.current_url
        if 'tutor' in url_address:
            self.tutor_logout(driver)
        elif 'accounts' in url_address:
            self.accounts_logout(driver)
        else:
            raise HTTPError('Not an OpenStax URL')

    def open_user_menu(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """
        Hamburger (user) menu opener.

        ToDo: branching to handle if a toggle is already open
        """
        wait = WebDriverWait(driver, wait_time)
        if driver.get_window_size('width') <= StaxHelper.CONDENSED_WIDTH:
            # compressed window display on Tutor
            wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'navbar-toggle')
                )
            ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'dropdown-toggle')
            )
        ).click()

    def tutor_logout(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Tutor logout helper."""
        self.open_user_menu(driver, wait_time)
        WebDriverWait(driver, wait_time).until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[@aria-label="Sign out"]')
            )
        ).click()

    def accounts_logout(self, driver):
        """OS Accounts logout helper."""
        driver.find_element(By.LINK_TEXT, 'Sign out').click()

    def select_course(self, driver, title=None, appearance=None,
                      wait_time=DEFAULT_WAIT_TIME):
        """Select course."""
        if 'dashboard' not in driver.current_url:
            return
        if title:
            uses_option = 'title'
            course = title.lower()
        elif appearance:
            uses_option = 'appearance'
            course = appearance.lower()
        else:
            raise self.LoginError('Unknown course selection "%s"' %
                                  title if title else appearance)
        WebDriverWait(driver, wait_time).until(
            expect.element_to_be_clickable(
                (
                    By.XPATH, '//div[@data-%s="%s"]//a' %
                    (uses_option, course)
                )
            )
        ).click()

    def view_reference_book(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Access the reference book."""
        try:
            driver.find_element(
                By.XPATH, '//div/a[contains(@class,"view-reference-guide")]'
            ).click()
            return
        except:
            pass
        self.open_user_menu(driver, wait_time)
        driver.find_element(
            By.XPATH, '//li/a[contains(@class,"view-reference-guide")]'
        ).click()


class LoginError(Exception):
    """Login error exception."""

    def __init__(self, value):
        """Exception initializer."""
        self.value = value

    def __str__(self):
        """Return string of the exception text."""
        return repr(self.value)


class Teacher(User):
    """User extention for teachers."""

    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 use_env_vars=False):
        """Teacher initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['TEACHER_USER']
            password = os.environ['TEACHER_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super().__init__(username, password, site, email, email_username,
                         email_password)

    def add_assignment(self, driver, assignment, args):
        """Add an assignment."""
        assign = Assignment()
        assign.add[assignment](
            driver=driver,
            name=args['title'],
            description=args['description'],
            periods=args['periods'],
            state=args['status'],
            url=args['url'] if 'url' in args else None,
            reading_list=args['reading_list'] if 'reading_list' in args else
            None,
            problems=args['problems'] if 'problems' in args else None,
        )

    def change_assignment(self, driver, assignment, args):
        """Alter an existing assignment."""
        assign = Assignment()
        assign.edit[assignment](
            driver=driver,
            name=args['title'],
            description=args['description'],
            periods=args['periods'],
            state=args['status'],
            url=args['url'] if 'url' in args else None,
            reading_list=args['reading_list'] if 'reading_list' in args else
            None,
            problems=args['problems'] if 'problems' in args else None,
        )

    def delete_assignment(self, driver, assignment, args):
        """Delete an existing assignment (if available)."""
        assign = Assignment()
        assign.remove[assignment](
            driver=driver,
            name=args['title'],
            description=args['description'],
            periods=args['periods'],
            state=args['status'],
            url=args['url'] if 'url' in args else None,
            reading_list=args['reading_list'] if 'reading_list' in args else
            None,
            problems=args['problems'] if 'problems' in args else None,
        )

    def goto_menu_item(self, driver, item, wait_time=DEFAULT_WAIT_TIME):
        """Go to a specific user menu item."""
        if 'courses' in driver.current_url:
            self.open_user_menu(driver)
            WebDriverWait(driver, wait_time).until(
                expect.element_to_be_clickable(
                    (By.LINK_TEXT, item)
                )
            ).click()

    def goto_calendar(self, driver):
        """Return the teacher to the calendar dashboard."""
        try:
            return driver.find_element(
                By.XPATH, '//a[contains(@class,"navbar-brand")]'
            ).click()
        except:
            self.goto_menu_item('Dashboard')

    def goto_performance_forecast(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Access the performance forecast page."""
        self.goto_menu_item(driver, 'Performance Forecast', wait_time)

    def goto_student_scores(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Access the student scores page."""
        self.goto_menu_item(driver, 'Student Scores', wait_time)


class Student(User):
    """User extention for students."""

    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 use_env_vars=False):
        """Student initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['STUDENT_USER']
            password = os.environ['STUDENT_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super().__init__(username, password, site, email, email_username,
                         email_password)

    def work_assignment(self):
        """Work an assignment.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def goto_past_work(self):
        """View work for previous weeks.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def goto_performance_forecast(self):
        """View the student performance forecast.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

    def practice(self):
        """Complete a set of 5 practice problems.

        ToDo: all
        """
        raise NotImplementedError(inspect.currentframe().f_code.co_name)


class Admin(User):
    """User extention for administrators."""

    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 use_env_vars=False):
        """Administrator initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['ADMIN_USER']
            password = os.environ['ADMIN_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super().__init__(username, password, site, email, email_username,
                         email_password)

    def goto_admin_control(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Access the administrator controls."""
        wait = WebDriverWait(driver, wait_time)
        wait.until(
            expect.visibility_of_element_located(
                (
                    By.XPATH, '%s%s' %
                    ('//li[contains(@class,"-hamburger-menu")]/',
                     'a[@type="button"]')
                )
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Admin')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Admin Console"]')
            )
        )

    def goto_courses(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Access the course admin control."""
        wait = WebDriverWait(driver, wait_time)
        try:
            wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Admin Console"]')
                )
            )
        except:
            self.goto_admin_control(driver, wait_time)
        organization = wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Course Organization')
            )
        )
        if 'open' not in organization.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            organization.click()
        wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Courses"]')
            )
        )

    def goto_ecosystems(self, driver, wait_time=DEFAULT_WAIT_TIME):
        """Access the ecosystem admin control."""
        wait = WebDriverWait(driver, wait_time)
        try:
            wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Admin Console"]')
                )
            )
        except:
            self.goto_admin_control()
        content = wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Content')
            )
        )
        if 'open' not in content.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            content.click()
        wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Ecosystems')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Ecosystems"]')
            )
        )


class ContentQA(User):
    """User extention for content users."""

    DEFAULT_WAIT_TIME = User.DEFAULT_WAIT_TIME

    def __init__(self, username=None, password=None, site=None, email=None,
                 use_env_vars=False):
        """Content analyst initialization with User pass-through."""
        if use_env_vars:
            username = os.environ['CONTENT_USER']
            password = os.environ['CONTENT_PASSWORD']
            site = os.environ['SERVER_URL']
            email = os.environ['TEST_EMAIL_ACCOUNT']
            email_username = os.environ['TEST_EMAIL_USER']
            email_password = os.environ['TEST_EMAIL_PASSWORD']
        super().__init__(username, password, site, email, email_username,
                         email_password)

# ########################################################################### #


class TestStaxHelper(unittest.TestCase):
    """Unit tests for helper classes."""

    def test_staxhelper_chrome(self):
        """Start a Chrome instance."""
        try:
            helper = StaxHelper().quit()
            helper = StaxHelper(initial_user=User())
            helper.quit()
            helper = StaxHelper(driver_type='chrome').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> Chrome Driver not available <')
        finally:
            if bool(helper.driver):
                helper.driver.quit()

    def test_staxhelper_firefox(self):
        """Start a Firefox instance."""
        try:
            StaxHelper(driver_type='firefox').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> FireFox Driver not available <')

    @unittest.skipIf(sys.platform == 'darwin', 'No IE on Mac')
    def test_staxhelper_ie(self):
        """Start an Internet Explorer instance."""
        try:
            StaxHelper(driver_type='ie').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> Internet Explorer Driver not available <')

    def test_staxhelper_opera(self):
        """Start an Opera instance."""
        try:
            StaxHelper(driver_type='opera').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> Opera Driver not available <')

    @unittest.skipIf(True, 'PhantomJS is not implemented')
    def test_staxhelper_phantomjs(self):
        """Start a PhantomJS instance."""
        try:
            StaxHelper(driver_type='phantomjs').quit()
        except FileNotFoundError or WebDriverException:
            print('\n> PhantomJS Driver not available <')

    def test_staxhelper_init_errs(self):
        """Assertion testing."""
        with self.assertRaises(TypeError):
            StaxHelper(driver_type='saucelabs')
        with self.assertRaises(StaxHelper.WebDriverTypeException):
            StaxHelper(driver_type='no driver type')


class TestUser(unittest.TestCase):
    """Test the base User class."""

    def setUp(self):
        """Test case setup."""
        self.user = User()
        self.helper = StaxHelper(initial_user=self.user)

    def tearDown(self):
        """Test case cleanup."""
        self.helper.quit()

    def test_user_object(self):
        """Test a default User object."""
        assert(self.user.username is None), 'Username is set'
        assert(self.user.password is None), 'Password is set'
        assert(self.user.url is not None), 'URL is not parsed or is invalid'
        assert(self.user.email is None), 'E-mail is set'

    def test_user_login(self):
        """Test a generic login."""
        self.user.login('student01',
                        'password',
                        'https://tutor-qa.openstax.org/')


class TestTeacherUser(unittest.TestCase):
    """Test the Teacher child object."""

    def setUp(self):
        """Test case setup."""
        self.user = Teacher()
        self.helper = StaxHelper(initial_user=self.user)

    def tearDown(self):
        """Test case cleanup."""
        self.helper.quit()


class TestStudentUser(unittest.TestCase):
    """Test the Student child object."""

    def setUp(self):
        """Test case setup."""
        self.user = Student()
        self.helper = StaxHelper(initial_user=self.user)

    def tearDown(self):
        """Test case cleanup."""
        self.helper.quit()


class TestAdminUser(unittest.TestCase):
    """Test the Admin child object."""

    def setUp(self):
        """Test case setup."""
        self.user = Admin()
        self.helper = StaxHelper(initial_user=self.user)

    def tearDown(self):
        """Test case cleanup."""
        self.helper.quit()


class TestContentQAUser(unittest.TestCase):
    """Test the Content child object."""

    def setUp(self):
        """Test case setup."""
        self.user = ContentQA()
        self.helper = StaxHelper(initial_user=self.user)

    def teardown(self):
        """Test case cleanup."""
        self.helper.quit()


class TestAssignments(unittest.TestCase):
    """Test the Assignments module."""

    def setUp(self):
        """Test case setup for assignment creation."""
        self.today = datetime.date.today()
        self.user = Teacher()
        self.helper = StaxHelper(initial_user=self.user)

    def tearDown(self):
        """Test case cleanup."""
        self.helper.quit()

    def test_assignments(self):
        """Test assignment creation."""
        begin = (self.today + datetime.timedelta(days=0)).strftime('%m/%d/%Y')
        end = (self.today + datetime.timedelta(days=3)).strftime('%m/%d/%Y')
        # start the code example
        self.user.login()
        self.user.select_course(category='physics')
        for chap in ['ch11', 'ch12']:
            reading = 'v6.131 chapter %s' % chap
            self.user.add_assignment(
                assignment='reading',
                args={
                    'title': reading,
                    'description': 'A diagnostic assignment for %s' % chap,
                    'periods': {'all': (begin, end)},
                    'reading_list': [chap],
                    'status': 'publish',
                }
            )
            sleep(5)
        homework = 'test-hw %s' % Assignment.rword(8)
        self.user.add_assignment(
            assignment='homework',
            args={
                'title': homework,
                'description': 'An auto-test assignment',
                'periods': {'all': (begin, end)},
                'problems': {'4': None,
                             '4.1': (4, 8),
                             '4.2': 'all',
                             '4.3': ['2102@1', '2104@1', '2175'],
                             'ch5': 5,
                             'tutor': 4},
                'status': 'draft',
            }
        )


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()
