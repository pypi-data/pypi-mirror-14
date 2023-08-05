"""Tutor teacher test cases."""

import unittest
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, date

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
class TestTutorTeacher(unittest.TestCase):
    """Teacher test cases."""

    def setUp(self):
        """Test case setup routine."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.teacher = Teacher(use_env_vars=True)
        self.helper = StaxHelper(driver_type='saucelabs', pasta_user=self.ps,
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
        """Test case cleanup and reporting."""
        session = self.driver.session_id
        # Returns the info of exception being handled
        has_errors = self._test_has_failed()
        if has_errors:
            print(self.driver.current_url, '\n')
            date_and_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            filename = 'testerr_%s.png' % date_and_time
            self.driver.save_screenshot('%s%s' % (self.screenshot_path,
                                        filename))
        try:
            self.driver = None
            self.helper.driver.quit()
        except AttributeError:
            pass
        self.ps.update_job(session, passed=not has_errors)

    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def test_teacher_views_calendar(self):
        ''''''
        today = date.today()
        today = today.strftime('%B %Y')
        cal_date = self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"calendar-header-label")]' +
                 '/span')
            )
        ).text
        assert(cal_date == today), 'Calendar date is not %s' % today

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_student_scores(self):
        ''''''
        # click on student scores
        self.helper.user.goto_student_scores(self.driver)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reference_book(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_roster(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_removes_a_student_from_class(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_moves_a_student_between_periods(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reading_analytics_aggregate(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_performance_forecast_aggregate(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_performance_forecast(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_external_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_homework_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reading_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_event_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_review_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_homework(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_homework_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_reading(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_reading_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_review(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_review_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_export_matches_student_scores(self):
        ''''''
