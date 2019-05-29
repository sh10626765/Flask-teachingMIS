from flask import *
from SQL_method import *


student_list = []
teacher_list = []
admin_list = []
course_list = []
opencourse_list = []

lesson_open_by_teacher = []
grades_info = []
stugra_info = []

courses_info = []
students = []
teachers = []
courses = []
ranklist = []
data = []

app = Flask(__name__)


def varStugraInfo():
    global stugra_info
    return stugra_info
def setStugraInfo(s):
    global stugra_info
    stugra_info = s


def varGradeInfo():
    global grades_info
    return grades_info
def setGradeInfo(s):
    global grades_info
    grades_info = s


def varLessonOpenByTeacher():
    global lesson_open_by_teacher
    return lesson_open_by_teacher
def setLessonOpenByTeacher(s):
    global lesson_open_by_teacher
    lesson_open_by_teacher = s


def varStudents():
    global students
    return students
def setStudents(s):
    global students
    students = s


def varTeachers():
    global teachers
    return teachers
def setTeachers(s):
    global teachers
    teachers = s


def varCourses():
    global courses
    return courses
def setCourses(s):
    global courses
    courses = s


def varData():
    global data
    return data
def setData(s):
    global data
    data = s


def varRanklist():
    global ranklist
    return ranklist
def setRanklist(s):
    global ranklist
    ranklist = s


def varCourseinfo():
    global courses_info
    return courses_info
def setCourseinfo(s):
    global courses_info
    courses_info = s


def varAdminlist():
    global admin_list
    return admin_list
def setAdminlist(s):
    global admin_list
    admin_list = s


def varStudentlist():
    global student_list
    return student_list
def setStudentlist(s):
    global student_list
    student_list = s


def varTeacherlist():
    global teacher_list
    return teacher_list
def setTeacherlist(s):
    global teacher_list
    teacher_list = s


def varOpencourselist():
    global opencourse_list
    return opencourse_list
def setOpencourselist(s):
    global opencourse_list
    opencourse_list = s


def varCourselist():
    global course_list
    return course_list
def setCourselist(s):
    global course_list
    course_list = s


def computeGPA(s):
    if not s:
        return 'nul'
    else:
        if 100 >= int(s) >= 90:
            return 4.0
        elif 89 >= int(s) >= 85:
            return 3.7
        elif 84 >= int(s) >= 82:
            return 3.3
        elif 81 >= int(s) >= 78:
            return 3.0
        elif 77 >= int(s) >= 75:
            return 2.7
        elif 74 >= int(s) >= 72:
            return 2.3
        elif 71 >= int(s) >= 68:
            return 2.0
        elif 67 >= int(s) >= 64:
            return 1.5
        elif 63 >= int(s) >= 60:
            return 1.0
        elif 59 >= int(s) >= 9:
            return 0
