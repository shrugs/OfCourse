
# from bs4 import BeautifulSoup as BS
import peewee
from peewee import *
import re

db = MySQLDatabase('OfCourse', user='OfCourse',passwd='')


class Departments(peewee.Model):
    DeptID = PrimaryKeyField(primary_key=True, auto_increment=True)
    Dept = CharField(100)

    class Meta:
        database = db

class Subjects(peewee.Model):
    SubjectID = CharField(primary_key=True)
    Subject = CharField(150)

    class Meta:
        database = db

class Colleges(peewee.Model):
    CollegeID = peewee.PrimaryKeyField(primary_key=True)
    College = peewee.CharField(100)

    class Meta:
        database = db

class Courses(peewee.Model):
    CourseID = peewee.PrimaryKeyField(primary_key=True)
    Course = peewee.CharField(100)
    CollegeID = ForeignKeyField(Colleges, related_name='collegeID')
    CourseCode = CharField(20)
    CreditsMax = IntegerField()
    CreditsMin = IntegerField()
    Description = TextField()
    DeptID = ForeignKeyField(Departments, related_name="deptID")
    SubjectID = ForeignKeyField(Subjects, related_name="subjectID")

    class Meta:
        database = db

def find_key(key, text):
    new_re = '\<!-- \"' + key + '\"-->\n\<!-- \"(?P<value>.+)\"--\>'
    m = re.search(new_re, text)
    if (m):
        return m.group('value').strip()
    else:
        return ""

def find_all_keys(key, text):
    new_re = '\<!-- \"' + key + '\"-->\n\<!-- \"(?P<value>.+)\"--\>'
    m = re.finditer(new_re, text)
    s = ""
    for subs in m:
        s += subs.group('value')

    return s

if False:
    Departments.create_table()
    Subjects.create_table()
    Colleges.create_table()
    Courses.create_table()

with open('logged_subjects.txt') as f:
    subjects = f.readlines()

done = False

for subject in subjects:
    if done:
        break
    subject = subject.rstrip()

    try:
        with open(subject + '.html') as h:
            h = h.read()
            print "PARSING: " + subject + "\n"
            # page = BS(h)
            if ("There is no information for the subject you have selected." in h):
                print "No information :(\n"
                continue

            re_course_info_comments_start = re.compile("""\<!-- \"\"-->\n<!-- \"\"--\>""")
            course_info_comments_start = re_course_info_comments_start.search(h)
            start_index = course_info_comments_start.start()

            # <!-- Campus pipeline not enabled-->
            re_course_info_comments_end = re.compile("""\<!-- Campus pipeline not enabled-->""")
            course_info_comments_end = re_course_info_comments_end.search(h)
            end_index = course_info_comments_end.start()

            h = h[start_index:end_index]
            # print h

            # get subject name
            Subject = find_key('ColCatHdrSubject', h)

            try:
                db_subject = Subjects.select().where(Subjects.SubjectID == subject).get()
            except:
                db_subject = Subjects.create(SubjectID=subject, Subject=Subject)


            CourseID_indexes = []
            for m in re.finditer("""\<!-- \"CourseID\"--\>""", h):
                CourseID_indexes.append(m.start())

            print CourseID_indexes
            c = len(CourseID_indexes)
            for i, CourseID in enumerate(CourseID_indexes):
                # for each CourseID, grab its value and the next on
                this_course_index = CourseID
                if (i <= c-2):
                    next_course_index = CourseID_indexes[i+1]
                    this_course = h[this_course_index:next_course_index]
                    # print str(this_course_index) + "->" + str(next_course_index) + "\n"
                else:
                    this_course = h[this_course_index:]
                    print "FINAL\n"

                # print this_course
                # print "\n\n"
                CourseCode = find_key("CourseID", this_course)
                CourseName = find_key("CourseTitle", this_course)
                College = find_key("College", this_course)
                Department = find_key("Dept", this_course)
                Credit = find_key("Credit", this_course)
                CourseCtr = find_key("CourseCtr", this_course)
                SubjectDescription = find_key("SubjDesc", this_course)
                Description = find_all_keys("ItemLine", this_course)

                if ('to' in Credit):
                    cred = Credit.split('to')
                    CreditsMax = float(cred[1].strip())
                    CreditsMin = float(cred[0].strip())
                else:
                    CreditsMin = float(Credit.strip())
                    CreditsMax = CreditsMin

                # DEPT
                try:
                    db_dept = Departments.select().where(Departments.Dept == Department).get()
                except:
                    db_dept = Departments.create(Dept=Department)


                # COLLEGE
                try:
                    db_college = Colleges.select().where(Colleges.College == College).get()
                except:
                    db_college = Colleges.create(College=College)

                # COURSE
                try:
                    db_course = Courses.select().where(Courses.CourseCode == CourseCode).get()
                except:
                    db_course = Courses.create(CourseCode=CourseCode,
                                               Course=CourseName,
                                               CollegeID=db_college.CollegeID,
                                               CreditsMax=CreditsMax,
                                               CreditsMin=CreditsMin,
                                               Description=Description,
                                               DeptID=db_dept.DeptID,
                                               SubjectID=db_subject.SubjectID)


                print "Course: " + CourseName


            # done = True
    except IOError:
        print "No content: " + subject
        pass