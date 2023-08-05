import unittest
# import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper, Teacher
try:
    from . import Assignment
except:
    from staxing.assignment import Assignment

# NOT_STARTED = True

browsers = [{
    "platform": "Windows 7",
    "browserName": "firefox",
    "version": "40.0",
    "screenResolution": "1440x900"
}]

standard_window = (1440, 800)
compressed_window = (700, 500)


@PastaDecorator.on_platforms(browsers)
class TestTutorAccountManagement(unittest.TestCase):
    ''''''
    def setUp(self):
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(use_env_vars=True)
        self.helper = StaxHelper(driver_type='chrome', pasta_user=self.ps,
                                 capabilities=self.desired_capabilities,
                                 initial_user=self.teacher)
        self.driver = self.helper.driver
        self.wait = WebDriverWait(self.driver, StaxHelper.DEFAULT_WAIT_TIME)
        self.driver.set_window_size(*standard_window)
        # self.teacher.login(self.driver)
        # self.teacher.select_course(self.driver, category='physics')
        self.rword = Assignment.rword
        self.screenshot_path = '/tmp/errors/'

    def tearDown(self):
        # Returns the info of exception being handled
        has_errors = self._test_has_failed()
        if has_errors:
            print(self.driver.current_url, '\n')
            date_and_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            filename = 'testerr_%s.png' % date_and_time
            self.driver.save_screenshot('%s%s' % (self.screenshot_path,
                                        filename))
        self.driver.quit()
        self.ps.update_job(self.driver.session_id, passed=has_errors)

    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def test_user_registration(self):
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in ' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.LINK_TEXT, 'Sign up').click()
        username = 'testuser_%s' % self.rword(5)
        first_name = 'Test User'
        last_name = self.rword(6)
        email = self.teacher.email
        self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'register_username')
            )
        ).send_keys(username)
        self.driver.find_element(By.ID, 'register_email'). \
            send_keys(email)
        self.driver.find_element(By.ID, 'register_password'). \
            send_keys('password')
        self.driver.find_element(By.ID, 'register_password_confirmation'). \
            send_keys('password')
        self.driver.find_element(
            By.XPATH, '//input[@class="standard" and @name="commit"]'
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Continue')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'register_username')
            )
        )
        self.driver.find_element(By.ID, 'register_title'). \
            send_keys(self.rword(2))
        self.driver.find_element(By.ID, 'register_first_name'). \
            send_keys(first_name)
        self.driver.find_element(By.ID, 'register_last_name'). \
            send_keys(last_name)
        self.driver.find_element(By.ID, 'register_suffix'). \
            send_keys(self.rword(2))
        self.driver.find_element(By.ID, 'register_full_name'). \
            send_keys('%s %s' % (first_name, last_name))
        self.driver.find_element(By.LINK_TEXT, 'Terms of Use').click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[@class="close"]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Privacy Policy')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[@class="close"]')
            )
        ).click()
        i_agree = self.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'register_i_agree')
            )
        )
        submit = self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'register_submit')
            )
        )
        if submit.get_attribute('class') != 'standard':
            i_agree.click()
        submit.click()
        assert('Your Account' in self.driver.title), 'Incorrect URL: %s' % \
            self.driver.current_url

    def test_user_login_standard(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: %sx%s, not %sx%s' %
             (size['width'], str(*size)))
        # open the test URL and click the login button
        self.driver.get(self.teacher.url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.teacher.username)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.teacher.password)
        # click on the sign in button to log in
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        # look for the user drop down menu and click to open it
        self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'dropdown-toggle')
            )
        ).click()
        # is the log out link visible?
        logout = self.driver.find_element(By.CLASS_NAME, 'logout')
        assert('Log Out' in logout.text), 'Log out not visible'

    def test_user_login_compact(self):
        # resize the window to be closer to a mobile display width
        self.driver.set_window_size(*compressed_window)
        size = self.driver.get_window_size()
        assert(compressed_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*compressed_window))
        # open the test URL and click the login button within the sub-menu
        self.driver.get(self.helper.user.url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        user_menu = self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'navbar-toggle')
            )
        )
        assert(user_menu.is_displayed()), 'Menu not visible'
        user_menu.click()
        login = self.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        )
        assert(login.is_displayed()), 'Login link not visible'
        login.click()
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.user.username)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.user.password)
        # click on the sign in button to log in
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]').click()
        # look for the user drop down menu and click to open it
        user_menu = self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'navbar-toggle')
            )
        )
        assert(user_menu.is_displayed()), 'User menu not visible'
        user_menu.click()

    def test_accounts_login(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        # open the test URL and click the login button within the sub-menu
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in ' in self.driver.title), 'Unable to load page'
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.user.username)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.user.password)
        # click on the sign in button to log in
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]').click()
        # is the logged in user's login visible?
        self.driver.find_element(
            By.LINK_TEXT, self.helper.user.username).click()

    def test_account_login_failure(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in ' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys('not_a_user_94720475')
        self.driver.find_element(By.ID, 'password'). \
            send_keys('failed_password')
        self.driver.find_element(By.XPATH,
                                 '//button[text()="Sign in"]').click()
        error_message = self.driver.find_element(By.XPATH,
                                                 '//p//strong/parent::*')
        assert('Incorrect' in error_message.text)

    def test_course_select(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.get(self.helper.user.url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        login = self.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        )
        assert(login.is_displayed()), 'Login link not visible'
        login.click()
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.user.username)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.user.password)
        self.driver.find_element(By.XPATH, '//button[text()="Sign in"]'). \
            click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[contains(@data-title, "Physics")]//a')
            )
        ).click()
        dashboard = self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[@class="navbar-brand active"]')
            )
        )
        assert('Physics' in dashboard.text)

    def test_password_reset(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.set_window_size(*standard_window)
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in ' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.LINK_TEXT, 'Forgot password?').click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'forgot_password_username_or_email')
            )
        ).send_keys(self.helper.user.username)
        self.driver.find_element(By.NAME, 'commit').click()
        self.helper.sleep(4.5)
        try:
            self.driver.find_element(
                By.XPATH, '//p[contains(text(),"No verified email")]'
            )
            assert(False), 'No verified email - stubbed for now'
        except:
            pass
        reset_message = self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"ui-icon-info")]')
            )
        )
        reset_message = reset_message.find_element(By.XPATH, '..')
        assert('Password reset' in reset_message.text), 'Reset failed'
        body = self.driver.find_element(By.TAG_NAME, 'body')
        import platform
        if platform.system() == 'Darwin':  # Mac
            body.send_keys(Keys.COMMAND + 't')
        else:
            body.send_keys(Keys.CONTROL + 't')
        self.driver.get('https://mail.google.com/')
        assert('Gmail' in self.driver.title), 'Gmail login not available'
        username = self.driver.find_element(By.ID, 'Email')
        username.send_keys(self.teacher.email)
        next_button = self.driver.find_element(By.ID, 'next')
        next_button.click()
        password = self.driver.find_element(By.ID, 'Passwd')
        password.send_keys(self.teacher.email_password)
        stay_signed_in = self.driver.find_element(By.ID, 'PersistentCookie')
        if stay_signed_in.is_selected():
            stay_signed_in.click()
        next_button = self.driver.find_element(By.ID, 'signIn')
        next_button.click()
        try:
            reset_email = self.wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'y6')
                )
            )
        except:
            assert(False), 'Email message not received'
        reset_email.click()
        try:
            reset_link = self.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//a[contains(@href, "accounts-qa")]')
                )
            )
        except:
            assert(False), 'Wrong e-mail message selected'
        link = reset_link.get_attribute('href')
        self.driver.find_element(
            By.XPATH,
            '//a[@title="Gmail" and contains(@href,"inbox")]'
        ).click()
        reset_email = self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'y6')
            )
        )
        trash_can = self.driver.find_element(By.LINK_TEXT, 'Trash')
        chain = ActionChains(self.driver). \
            move_to_element(reset_email). \
            drag_and_drop(reset_email, trash_can)
        chain.perform()
        self.driver.close()
        self.driver = StaxHelper.run_on(
            StaxHelper.LOCAL, self.ps, self.desired_capabilities
        )
        self.driver.implicitly_wait(15)
        self.driver.set_window_size(*standard_window)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get(link)
        new_password = self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//input[@name="reset_password[password]"]')
            )
        )
        new_password.send_keys(self.teacher.password)
        repeat_password = self.driver.find_element(
            By.ID, 'reset_password_password_confirmation'
        )
        repeat_password.send_keys(self.teacher.password)
        submit = self.driver.find_element(By.NAME, 'commit')
        submit.click()
        reset_message = self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'ui-icon-info')
            )
        )
        reset_message = reset_message.find_element(By.XPATH, '..')
        assert('reset successfully' in reset_message.text)

    def test_ost_logo_click_user_not_logged_in(self):
        url = 'https://tutor-qa.openstax.org/'
        anchor = '#home'
        self.driver.get(url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//a[@class="navbar-brand" and @href="%s"]' % anchor)
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//a[@class="navbar-brand" and @href="%s"]' % anchor)
            )
        )
        full_url = url + anchor
        assert(self.driver.current_url == full_url), 'Not at dashboard'

    def test_ost_logo_click_user_logged_in(self):
        self.helper.user.login(self.driver,
                               self.helper.user.username,
                               self.helper.user.password)
        url = self.helper.user.url
        if url[-1:] == '/':
            url = url[:-1]
        route = '/dashboard/'
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//a[contains(@class,"navbar-brand") ' +
                 'and @href="%s"]' % route)
            )
        ).click()
        local_wait = WebDriverWait(self.driver, 5)
        try:
            local_wait.until(
                expect.element_to_be_clickable(
                    (By.CLASS_NAME, 'tutor-course-item')
                )
            )
        except:
            assert('calendar' in self.driver.current_url), 'Not at calendar'
        full_url = url + route
        assert(self.driver.current_url == full_url), 'Not at dashboard'

    def test_user_updates_profile_information(self):
        self.helper.user.login(self.driver,
                               self.helper.user.username,
                               self.helper.user.password,
                               'https://accounts-qa.openstax.org/')
        heading = self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'page-heading')
            )
        )
        new_title = self.rword(3)
        new_suffix = self.rword(2)
        assert(heading.text == 'Your Account'), 'Not at the profile control'
        self.driver.find_element(By.ID, 'user_title').clear()
        self.driver.find_element(By.ID, 'user_title'). \
            send_keys(new_title)
        self.driver.find_element(By.ID, 'user_suffix').clear()
        self.driver.find_element(By.ID, 'user_suffix'). \
            send_keys(new_suffix)
        self.driver.find_element(
            By.XPATH, '//input[contains(@value,"Update Profile")]').click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class,"ui-icon")]')
            )
        )
        title = self.driver.find_element(By.ID, 'user_title')
        assert(title.get_attribute('value') == new_title), \
            'Change to the title failed'
        suffix = self.driver.find_element(By.ID, 'user_suffix')
        assert(suffix.get_attribute('value') == new_suffix), \
            'Change to the suffix failed'

    def test_user_email_management(self):
        self.helper.user.login(self.driver,
                               self.helper.user.username,
                               self.helper.user.password,
                               'https://accounts-qa.openstax.org/')
        heading = self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'page-heading')
            )
        )
        assert(heading.text == 'Your Account'), 'Not at the profile control'
        print('At Account control')
        self.driver.find_element(By.LINK_TEXT, 'Manage Email Addresses'). \
            click()
        print('Retrieve e-mails')
        emails = self.driver.find_elements(By.XPATH,
                                           '//tr/td[contains(text(),"@")]')
        for email in emails:
            print(email.text)
            if self.teacher.email in email.text:
                print('Removing current e-mail to rerun the test')
                self.driver.find_element(
                    By.XPATH,
                    '//a[contains(@data-confirm,"%s")]' %
                    self.teacher.email
                ).click()
                self.driver.switch_to_alert().accept()
                print('E-mail cleared')
        self.driver.find_element(By.ID, 'contact_info_value'). \
            send_keys(self.teacher.email)
        self.driver.find_element(
            By.XPATH, '//input[@value="Add"]'
        ).click()
        print('Adding e-mail address')
        self.driver.get('https://mail.google.com/')
        assert('Gmail' in self.driver.title), 'Gmail login not available'
        print('Opening Gmail for confirmation e-mail')
        username = self.driver.find_element(By.ID, 'Email')
        username.send_keys(self.teacher.email)
        next_button = self.driver.find_element(By.ID, 'next')
        next_button.click()
        password = self.driver.find_element(By.ID, 'Passwd')
        password.send_keys(self.teacher.password)
        stay_signed_in = self.driver.find_element(By.ID, 'PersistentCookie')
        if stay_signed_in.is_selected():
            stay_signed_in.click()
        next_button = self.driver.find_element(By.ID, 'signIn')
        next_button.click()
        print('Signing in to Gmail')
        try:
            email_confirm = self.wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'y6')
                )
            )
        except Exception as ex:
            self.fail('Email message not received :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        finally:
            try:
                email_confirm.click()
            except UnboundLocalError as ex:
                assert(False), 'Error logging into Google :: %s :: %s' % \
                    (ex.__class__.__name__, ex)
        print('Opening message')
        try:
            confirmation = self.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//a[contains(@href, "accounts-qa")]')
                )
            )
        except Exception as ex:
            self.fail('Wrong e-mail message selected :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        link = confirmation.get_attribute('href')
        print('Save the confirmation URL')
        self.driver.close()
        self.driver = self.helper.run_on(self.ps, self.desired_capabilities)
        self.driver.implicitly_wait(15)
        self.driver.set_window_size(*standard_window)
        try:
            if self.wait:
                self.wait = None
        except:
            pass
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get(link)
        print('Open the confirmation URL')
        heading = self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'page-heading')
            )
        )
        assert('Verification' in heading.text), 'Email not verified'
        print('E-mail verified')
        self.teacher.login(self.driver,
                           self.teacher.username,
                           self.teacher.password,
                           'https://accounts-qa.openstax.org/')
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Manage Email Addresses')
            )
        ).click()
        try:
            email = self.driver.find_elements(By.XPATH,
                                              '//td[contains(text(),"@")]')
        except Exception as ex:
            self.fail('Email not found in verified list :: %s :: %s' %
                      (ex.__class__.__name__, ex))
