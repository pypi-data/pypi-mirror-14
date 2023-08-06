"""helper test."""

from time import sleep
from helper import Helper, Teacher, Student, Admin, ContentQA, User
from assignment import Assignment

print('HELPER CLASS')
helper = Helper()
helper.change_wait_time(5)
print(helper.wait_time)
print(helper.date_string())
print(helper.date_string(5))
print(helper.date_string(str_format='%Y-%m-%d'))
print(helper.date_string(12, '%Y%m%d'))
print('GET google.com')
helper.get('https://www.google.com/')
print(helper.get_window_size())
print(helper.get_window_size('height'))
print(helper.get_window_size('width'))
print('starting sleep 1')
helper.sleep()
print('ending sleep 1')
print('starting sleep 5')
helper.sleep(5)
print('ending sleep 5')
helper.delete()

print('USER CLASS')
user = User('', '', '')
x = user + """print('Tutor login')
user.login('https://tutor-qa.openstax.org', 'student01', 'password')
print('Tutor logout')
user.logout()
print('Accounts login')
user.login('https://accounts-qa.openstax.org', 'student02', 'password')
print('Accounts logout')
user.logout()
print('User login')
user.login('https://tutor-qa.openstax.org', 'student01', 'password')
print('Select course by title')
user.select_course(title='Biology I ')
print('Go to course list')
user.goto_course_list()
print('Select course by appearance')
user.select_course(appearance='Biology')
print('Open the reference book')
user.view_reference_book()
user.delete()"""
x = x + ''

print('TEACHER CLASS')
teacher = Teacher(use_env_vars=True)
print('Tutor login')
teacher.login()
print('Select course by title')
teacher.select_course(title='Biology I ')
sleep(5)
#    from random import randint
#    print('Add a reading assignment')
#    teacher.add_assignment(
#        'reading',
#        args={
#            'title': 'reading test %s' % randint(0, 100000),
#            'description': 'class test',
#            'periods': {'all': (teacher.date_string(),
#                                teacher.date_string(randint(0, 10)))},
#            'reading_list': ['ch1', 'ch2', '3.1'],
#           'status': 'publish',
#       }
#    )
print('Go to the performance forecast')
try:
    teacher.goto_performance_forecast()
    sleep(5)
except:
    print('No performance forecast in Concept Coach')
print('Go to the calendar')
teacher.goto_calendar()
sleep(5)
print('Go to the course roster')
teacher.goto_course_roster()
sleep(5)
print('Add a section to the class')
section = Assignment.rword(10)
teacher.add_course_section(section)
try:
    print('Enrollment Code: ', teacher.get_enrollment_code(section))
    sleep(5)
except:
    print('No enrollment code in Tutor')
teacher.delete()

student = Student()
student.delete()

admin = Admin()
admin.delete()

content = ContentQA()
content.delete()
