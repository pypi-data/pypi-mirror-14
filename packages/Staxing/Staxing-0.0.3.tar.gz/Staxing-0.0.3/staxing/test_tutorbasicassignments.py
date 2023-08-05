import unittest
import pytest
import inspect

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper, Teacher
try:
    from . import Assignment
except:
    from staxing.assignment import Assignment

browsers = [{
    "platform": "Windows 7",
    "browserName": "firefox",
    "version": "40.0",
    "screenResolution": "1440x900"
}]

standard_window = (1440, 800)
compressed_window = (700, 500)

NOT_STARTED = True


@PastaDecorator.on_platforms(browsers)
class TestTutorBasicAssignments(unittest.TestCase):
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
        self.teacher.login(self.driver)
        self.teacher.select_course(self.driver, title='physics')
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
        self.driver = None
        self.helper.quit()
        self.ps.update_job(self.driver.session_id, passed=has_errors)

    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_all_cancel(self):
        '''
        '''
        # all / 0 / 1 / 1S / Cancel
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 1'
        description = 'by period cancel'
        open_all = StaxHelper.date_string()
        due_all = StaxHelper.date_string(1)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    'all': (open_all, due_all), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_all_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 2'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_all_publish(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 3'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_by_period_cancel(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 4'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_by_period_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 5'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_today_by_period_publish(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 6'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_all_cancel(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 7'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_all_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 8'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_all_publish_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 9'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_by_period_cancel(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 10'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_by_period_draft_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 11'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_future_by_period_publish_and_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        print(inspect.currentframe().f_code.co_name)
        print(self.__class__.__name__)
        name = 'Automated 12'
        description = 'by period cancel'
        open_p1 = StaxHelper.date_string()
        due_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        due_p2 = StaxHelper.date_string(2)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, due_p1),
                    '2nd': (open_p2, due_p2), },
                readings=['1.1'],
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))
