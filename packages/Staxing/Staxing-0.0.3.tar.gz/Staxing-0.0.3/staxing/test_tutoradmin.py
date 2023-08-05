import unittest
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from time import sleep

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper, Admin
try:
    from . import Assignment
except:
    from staxing.assignment import Assignment

NOT_STARTED = True

browsers = [{
    "platform": "Windows 7",
    "browserName": "firefox",
    "version": "40.0",
    "screenResolution": "1440x900"
}]

standard_window = (1440, 800)
compressed_window = (700, 500)


@PastaDecorator.on_platforms(browsers)
class TestTutorAdmin(unittest.TestCase):
    def setUp(self):
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.admin = Admin(use_env_vars=True)
        self.helper = StaxHelper(driver_type='chrome', pasta_user=self.ps,
                                 capabilities=self.desired_capabilities,
                                 initial_user=self.admin)
        self.driver = self.helper.driver
        self.wait = WebDriverWait(self.driver, StaxHelper.DEFAULT_WAIT_TIME)
        self.driver.set_window_size(*standard_window)
        self.admin.login(self.driver)
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

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_imports_a_new_ecosystem_book(self):
        self.admin.goto_admin_control(self.driver)
        self.admin.goto_ecosystems(self.driver)
        assert(self.driver.find_element(By.XPATH,
               '//h1[text()="Ecosystems"]')), 'Ecosystems not found'
        table = self.driver.find_element(By.ID, 'main')
        rows = table.find_elements(By.XPATH, './table/tbody/tr')
        assert(len(rows) >= 1), 'No previous ecosystem found'
        cells = rows[-1].find_elements(By.TAG_NAME, 'td')
        assert(len(cells) >= 1), 'No table cells available'
        uuid = cells[-1].find_element(By.TAG_NAME, 'a'). \
            get_attribute('data-content')
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Import a new Ecosystem')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Import a new Ecosystem"]')
            )
        )
        self.driver.find_element(By.ID, 'cnx_id'). \
            send_keys(uuid)
        self.driver.find_element(By.ID, 'comments'). \
            send_keys('Auto-test created')
        self.driver.find_element(By.XPATH, '//button[text()="Import"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('Import not queued :: %s :: %s' % (ex.__class__.__name__,
                      ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_district(self):
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(.,"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Districts')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Manage districts"]')
                )
            )
        except Exception as ex:
            self.fail('District management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.LINK_TEXT, 'Add district').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Create a district"]')
                )
            )
        except Exception as ex:
            self.fail('District creation page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.ID, 'district_name'). \
            send_keys('Auto-test District %s' % self.rword(4))
        self.driver.find_element(By.XPATH, '//input[@name="commit"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('District not created :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_edits_a_district(self):
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Districts')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Manage districts"]')
                )
            )
        except Exception as ex:
            self.fail('District management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.driver.find_element(
                By.XPATH,
                '//td[contains(text(),"Auto-test")]' +
                '/following-sibling::td/a[text()="edit"]'
            ).click()
        except NoSuchElementException as ex:
            self.fail('No Auto-test element :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Edit district"]')
                )
            )
        except Exception as ex:
            self.fail('District edit page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        old = self.driver.find_element(By.ID, 'district_name'). \
            get_attribute('value')
        current = old[:-4] + self.rword(4)
        self.driver.find_element(By.ID, 'district_name').clear()
        self.driver.find_element(By.ID, 'district_name'). \
            send_keys(current)
        self.driver.find_element(By.XPATH, '//input[@name="commit"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('District not updated :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_deletes_a_district(self):
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Districts')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Manage districts"]')
                )
            )
        except Exception as ex:
            self.fail('District management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.driver.find_element(
                By.XPATH,
                '//td[contains(text(),"Auto-test")]' +
                '/following-sibling::td/a[text()="delete"]'
            ).click()
        except Exception as ex:
            self.fail('No Auto-test district element to remove :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.switch_to_alert().accept()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('District not deleted :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_school(self):
        ''''''
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Schools')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Manage schools"]')
                )
            )
        except Exception as ex:
            self.fail('School management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.LINK_TEXT, 'Add school').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Create a school"]')
                )
            )
        except Exception as ex:
            self.fail('School creation page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.ID, 'school_name'). \
            send_keys('Auto-test School %s' % self.rword(4))
        Select(self.driver.find_element(By.TAG_NAME, 'select')). \
            select_by_visible_text('OpenStax')
        self.driver.find_element(By.XPATH, '//input[@name="commit"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('School not created :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_edits_a_school(self):
        ''''''
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Schools')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Manage schools"]')
                )
            )
        except Exception as ex:
            self.fail('School management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.driver.find_element(
                By.XPATH,
                '//td[contains(text(),"Auto-test")]' +
                '/following-sibling::td/a[text()="edit"]'
            ).click()
        except NoSuchElementException as ex:
            self.fail('No Auto-test element :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Edit school"]')
                )
            )
        except Exception as ex:
            self.fail('School edit page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        old = self.driver.find_element(By.ID, 'school_name'). \
            get_attribute('value')
        current = old[:-4] + self.rword(4)
        self.driver.find_element(By.ID, 'school_name').clear()
        self.driver.find_element(By.ID, 'school_name'). \
            send_keys(current)
        Select(self.driver.find_element(By.TAG_NAME, 'select')). \
            select_by_visible_text('OpenStax')
        self.driver.find_element(By.XPATH, '//input[@name="commit"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('School not updated :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_deletes_a_school(self):
        ''''''
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Schools')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Manage schools"]')
                )
            )
        except Exception as ex:
            self.fail('School management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(
            By.XPATH,
            '//td[contains(text(),"Auto-test")]' +
            '/following-sibling::td/a[text()="delete"]'
        ).click()
        self.driver.switch_to_alert().accept()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('School not deleted :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_course(self):
        ''''''
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Courses"]')
                )
            )
        except Exception as ex:
            self.fail('Course management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.LINK_TEXT, 'Add Course').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="New Course"]')
                )
            )
        except Exception as ex:
            self.fail('Course creation page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.ID, 'course_name'). \
            send_keys('Auto-test Course %s' % self.rword(4))
        Select(self.driver.find_element(By.TAG_NAME, 'select')). \
            select_by_visible_text('OpenStax Ed')
        self.driver.find_element(By.XPATH, '//input[@name="commit"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('Course not created :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_edits_a_course(self):
        ''''''
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Courses"]')
                )
            )
        except Exception as ex:
            self.fail('Course management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.driver.find_element(
                By.XPATH,
                '//td[contains(text(),"Auto-test")]' +
                '/following-sibling::td/a[text()="Edit"]'
            ).click()
        except NoSuchElementException as ex:
            self.fail('No Auto-test element :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        old = self.driver.find_element(By.ID, 'course_name'). \
            get_attribute('value')
        current = old[:-4] + self.rword(4)
        self.driver.find_element(By.ID, 'course_name').clear()
        self.driver.find_element(By.ID, 'course_name'). \
            send_keys(current)
        Select(self.driver.find_element(By.TAG_NAME, 'select')). \
            select_by_visible_text('OpenStax Ed')
        self.driver.find_element(By.XPATH, '//input[@name="commit"]').click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class,"alert-info")]')
                )
            )
        except Exception as ex:
            self.fail('Course name not changed :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.driver.find_element(
                By.XPATH,
                '//td[contains(text(),"Auto-test")]' +
                '/following-sibling::td/a[text()="Edit"]'
            ).click()
        except Exception as ex:
            self.fail('No Auto-test element :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Teachers")]')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h3[contains(text(),"Assign teachers")]')
                )
            )
        except Exception as ex:
            self.fail('Assign Teachers page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        try:
            self.driver.find_element(By.XPATH, '//td[text()="demo_teacher"]')
        except:
            sleep(0.5)
            ActionChains(self.driver). \
                move_to_element(self.driver.find_element(
                    By.ID, 'course_teacher')). \
                click(). \
                send_keys('demo_teacher'). \
                send_keys(Keys.ARROW_DOWN). \
                perform()
            sleep(0.5)
            ActionChains(self.driver). \
                move_to_element(self.driver.find_element(
                    By.XPATH, '//ul[contains(@class,"ui-autocomplete")]')). \
                click(). \
                perform()
            try:
                self.wait.until(
                    expect.visibility_of_element_located(
                        (By.XPATH, '//div[contains(@class,"alert-info")]')
                    )
                )
            except Exception as ex:
                self.fail('Teacher not set :: %s :: %s' %
                          (ex.__class__.__name__, ex))
        self.wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Course content')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h3[text()="Select a course ecosystem"]')
                )
            )
        except Exception as ex:
            self.fail('Select Ecosystem page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Periods')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h3[text()="Periods"]')
                )
            )
        except Exception as ex:
            self.fail('Periods page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.wait.until(
            expect.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Student Roster')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h3[text()="Upload Student Roster"]')
                )
            )
        except Exception as ex:
            self.fail('Student Roster upload page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))
        self.driver.find_element(By.LINK_TEXT, 'Main Dashboard').click()
        self.admin.goto_admin_control(self.driver)
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(),"Organization")]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Courses')
            )
        ).click()
        try:
            self.wait.until(
                expect.visibility_of_element_located(
                    (By.XPATH, '//h1[text()="Courses"]')
                )
            )
        except Exception as ex:
            self.fail('Course management page not loaded :: %s :: %s' %
                      (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_adds_a_teacher_to_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_removes_a_teacher_from_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_add_period_to_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_changes_period_name(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_creates_a_new_user_account(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_adds_student_to_period(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_removes_student_from_a_course(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_moves_student_to_another_period(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_impersonates_a_teacher(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_admin_impersonates_a_student(self):
        ''''''
