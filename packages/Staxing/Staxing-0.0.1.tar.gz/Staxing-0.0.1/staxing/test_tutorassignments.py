import unittest
import pytest

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
class TestTutorAssignments(unittest.TestCase):
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
        self.teacher.select_course(self.driver, category='physics')
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

    # @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_draft_to_all_cancel_to_period_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Draft
        # 2nd / 0 / 1 / 1S
        # all / 0 / 1 / 1S / Cancel
        # 1st / 0 / 1 / 1S / Delete
        # 2nd / 0 / 1 / 1S
        name = 'Automated 2'
        description = 'by period draft to all cancel to period delete'
        open_p1 = StaxHelper.date_string()
        close_p1 = StaxHelper.date_string(1)
        open_p2 = StaxHelper.date_string(1)
        close_p2 = StaxHelper.date_string(2)
        open_all = StaxHelper.date_string()
        close_all = StaxHelper.date_string(1)
        try:
            self.assign.add_new_reading(
                driver=self.driver,
                title=name,
                description=description,
                periods={
                    '1st': (open_p1, close_p1),
                    '2nd': (open_p2, close_p2), },
                readings=['1.1'],
                status=self.assign.DRAFT, )
        except Exception as ex:
            self.fail('1: Add :: %s :: %s' % (ex.__class__.__name__, ex))
        try:
            self.assign.change_reading(
                driver=self.driver,
                title=name,
                periods={
                    'all': (open_all, close_all), },
                status=self.assign.CANCEL)
        except Exception as ex:
            self.fail('2: Edit :: %s :: %s' % (ex.__class__.__name__, ex))
        try:
            self.assign.remove_reading(
                driver=self.driver,
                title=name)
        except Exception as ex:
            self.fail('3: Remove :: %s :: %s' % (ex.__class__.__name__, ex))

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_draft_to_all_draft_to_delete(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Draft
        # 2nd / 1 / 2 / 1S
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_all_publish_fail(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 0 / 1 / 1S
        # all / 0 / 1 / 1S / Publish **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_delete_fail(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # 1st / 0 / 1 / 1S / Delete **
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_all_publish_to_delete_fail(self):
        '''
        '''
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 2 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_all_cancel_to_period_delete(self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # all / 1 / 2 / 1S / Cancel
        # 1st / 1 / 2 / 1S / Delete
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_status_by_period_publish_to_all_publish_to_delete(
            self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # all / 1 / 2 / 1S / Publish
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_by_period_publish_to_delete(self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 2 / 3 / 1S
        # 1st / 1 / 2 / 1S / Delete
        # 2nd / 2 / 3 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_by_period_publish_to_all_publish_to_delete(self):
        '''
        '''
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 2 / 3 / 1S
        # all / 1 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_cancel(self):
        '''
        '''
        # all / 0 / 1 / 1S / Cancel

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_period_cancel_to_all_delete(self):
        '''
        '''
        # all / 0 / 1 / 1S / Draft
        # 1st / 0 / 1 / 1S / Cancel
        # 2nd / 0 / 1 / 1S
        # all / 0 / 1 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_period_draft_to_delete(self):
        '''
        '''
        # all / 0 / 1 / 1S / Draft
        # 1st / 0 / 1 / 1S / Draft
        # 2nd / 1 / 2 / 1S
        # 1st / 0 / 1 / 1S / Delete
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_all_draft_to_delete(self):
        '''
        '''
        # all / 0 / 1 / 1S / Draft
        # all / 0 / 1 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Draft
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_publish_to_period_delete_fail(
            self):
        '''
        '''
        # all / 0 / 1 / 1S / Publish
        # 1st / 0 / 1 / 1S / Publish
        # 2nd / 0 / 1 / 1S
        # 1st / 0 / 1 / 1S / Delete **
        # 2nd / 0 / 1 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_publish_fail(self):
        '''
        '''
        # all / 0 / 1 / 1S / Publish
        # 1st / 0 / 1 / 1S / Publish **
        # 2nd / 0 / 1 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_delete_fail(self):
        '''
        '''
        # all / 0 / 1 / 1S / Publish
        # all / 0 / 1 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_dates_all_draft_to_cancel_to_delete(self):
        '''
        '''
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 1 / 1S / Cancel
        # all / 0 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_open_dates_all_draft_to_cancel_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Cancel
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_draft_to_cancel_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 2 / 3 / 1S / Cancel
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_dates_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 1 / 1S / Draft
        # all / 0 / 1 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_earlier_all_publish_to_publish_to_delete_fail(
            self):
        '''
        '''
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 1 / 1S / Publish
        # all / 0 / 1 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_due_later_all_publish_to_publish_to_delete_fail(self):
        '''
        '''
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 3 / 1S / Publish
        # all / 0 / 3 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_sections_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C - 1S / Draft
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C - 1S / Draft
        # all / 1 / 2 / 1C - 1S / Publish
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_draft_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C + 1S / Draft
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_draft_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Draft
        # all / 1 / 2 / 1S + 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Draft
        # all / 1 / 2 / 1C + 1S / Publish
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Draft
        # all / 1 / 2 / 1S + 1S / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_minus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C - 1S / Draft
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_open_dates_all_publish_to_draft_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_minus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S - 1S / Draft
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_ch_minus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C - 1S / Publish
        # all / 1 / 2 / 1C - 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # all / 2 / 3 / 1S / Publish
        # all / 2 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_sec_minus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S - 1S / Publish
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C + 1S / Draft
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_publish_to_draft_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Publish
        # all / 1 / 2 / 1S + 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_plus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1C  / Publish
        # all / 1 / 2 / 1C + 1S / Publish
        # all / 1 / 2 / 1C + 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_draft_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Draft
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_publish_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Draft
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_chapter_all_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Publish
        # all / 1 / 2 / 1C / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_section_plus_sections_all_publish_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 1S  / Publish
        # all / 1 / 2 / 1S + 1S / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_open_dates_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Draft
        # all / 0 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_minus_sections_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S - 1S / Draft
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 2 / 3 / 1S / Draft
        # all / 2 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Draft
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_cancel_to_all_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # 1st / 1 / 2 / 1S / Cancel
        # 2nd / 1 / 2 / 1S
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_period_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # 1st / 1 / 2 / 1S / Publish
        # 2nd / 1 / 2 / 1S
        # 1st / 1 / 2 / 1S / Delete
        # 2nd / 1 / 2 / 1S

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_publish_to_delete_fail(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # all / 0 / 2 / 1S / Publish
        # all / 0 / 2 / 1S / Delete **

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 1S / Publish
        # all / 1 / 2 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_minus_section_all_draft_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S - 1S / Publish
        # all / 1 / 2 / 1S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_dates_all_draft_to_publish_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S + 1S / Draft
        # all / 1 / 2 / 3S - 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_publish_to_draft_to_publish_to_delete(
            self):
        '''
        '''
        # all / 1 / 2 / 2S  / Draft
        # all / 1 / 2 / 2S + 1S / Publish
        # all / 1 / 2 / 3S - 1S / Draft
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S + 1S / Draft
        # all / 1 / 2 / 3S - 1S / Draft
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 1 / 2 / 2S  / Publish
        # all / 1 / 2 / 2S + 1S / Publish
        # all / 1 / 2 / 3S - 1S / Publish
        # all / 1 / 2 / 2S  / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_draft_to_draft_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Draft
        # all / 1 / 3 / 1S / Delete

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_all_publish_to_publish_to_delete(self):
        '''
        '''
        # all / 2 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Publish
        # all / 1 / 3 / 1S / Delete
