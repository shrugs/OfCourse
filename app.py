#!/home/Envs/OfCourse/bin/python
from flask import Flask, render_template, url_for, request, jsonify, send_file, redirect, abort
import peewee
from peewee import *
from flask_peewee.rest import RestAPI, RestResource
import re

db = MySQLDatabase('OfCourse', user='OfCourse', passwd='OfCourseOfCourse')


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


def get_obj_ref(s):
    # would have been better to use a dictionary here and done return dict[s]
    if (s == 'course' or s == 'courses'):
        r = "Courses";
    elif (s == 'college' or s == 'colleges'):
        r = "Colleges";
    elif (s == 'dept' or s == 'depts'):
        r = "Departments"
    elif (s == 'subject' or s == 'subjects'):
        r = "Subjects";

    return r;

def get_values_from_peewee_clause(clause, obj_type):
    r = []
    for t in clause:
        a = {}
        for prop,val in vars(t).iteritems():
            if prop == "_data":
                a = val
            break
        print "yrs"
        a['type'] = obj_type
        a['id'] = a[obj_type+'ID']
        a['text'] = a[obj_type]
        print "end"
        r.append(a)
    return r

app = Flask(__name__)

class SubjectsResource(RestResource):
    paginate_by = 200

api = RestAPI(app)
api.register(Departments, SubjectsResource)
api.register(Courses)
api.register(Subjects, SubjectsResource)
api.register(Colleges, SubjectsResource)

api.setup()


@app.route('/')
def index():
    return render_template('latech.html',
                           require=url_for('static', filename='require.min.js'),
                           js=url_for('static', filename='latech.js'),
                           css=url_for('static', filename='latech.css'),
                           mainjs=url_for('static', filename='main.js'))

@app.route('/img/<i>')
def img(i):
    return send_file('static/js/'+str(i), mimetype='image/gif')


@app.route('/api/search')
def search():
    q = request.args.get('q', 'engineering')
    q = "%" + q.replace(' ', '%') + "%";
    print q
    r = []

    try:
        for t in Courses.select().where(Courses.CourseCode ** q | Courses.Course ** q | Courses.Description ** q).limit(100):
            # print t.Course
            a = {}
            for prop,val in vars(t).iteritems():
                if prop == "_data":
                    a = val
                break
            a['type'] = 'Course'
            a['id'] = a['CourseID']
            a['text'] = a['Course']
            r.append(a)
    except:
        print "except 1"
        pass
    try:
        for t in Colleges.select().where(Colleges.College ** q).limit(100):
            a = {}
            for prop,val in vars(t).iteritems():
                if prop == "_data":
                    a = val
                break

            a['type'] = 'College'
            a['id'] = a['CollegeID']
            a['text'] = a['College']
            r.append(a)
    except:
        print "except 2"
        pass
    try:
        for t in Subjects.select().where(Subjects.Subject ** q).limit(100):
            a = {}
            for prop,val in vars(t).iteritems():
                if prop == "_data":
                    a = val
                break

            a['type'] = 'Subject'
            a['id'] = a['SubjectID']
            a['text'] = a['Subject']
            r.append(a)
    except:
        print "except 3"
        pass
    try:
        for t in Departments.select().where(Departments.Dept ** q).limit(100):
            a = {}
            for prop,val in vars(t).iteritems():
                if prop == "_data":
                    a = val
                break

            a['type'] = 'Dept'
            a['id'] = a['DeptID']
            a['text'] = a['Dept']
            r.append(a)
    except:
        print "except 4"
        pass

    return jsonify({"values": r})

@app.route('/api/query')
def query():
    q = request.args.get('q', 'engineering')
    q = q.lower().strip()
    # print "QUERY: " + q
    new_re = '^(?P<return_obj_type>.+) (in|for) (?P<restriction_obj>.+)'
    m = re.search(new_re, q)
    # print m
    if m:
        return_obj_type = m.group('return_obj_type').strip()
        r_text = m.group('restriction_obj').strip()
        r = get_obj_ref(return_obj_type)

        values = []
        # for c in [Courses, Colleges, Subjects, Departments]:
            # if (c == Courses):
        if (r == "Courses"):
            values.append(get_values_from_peewee_clause(Courses.select().where(Courses.Course ** r_text | Courses.CourseCode ** r_text | Courses.Description ** r_text), "Course"))
        else:
            values.append(get_values_from_peewee_clause(Courses.select().join(Courses).where(Courses.Course ** r_text | Courses.CourseCode ** r_text | Courses.Description ** r_text), "Course"))

            # elif (c == Colleges):
        if (r == "Colleges"):
            values.append(get_values_from_peewee_clause(Colleges.select().where(Colleges.College ** r_text), "College"))
        else:
            values.append(get_values_from_peewee_clause(Colleges.select().join(Colleges).where(Colleges.College ** r_text), "College"))

            # elif (c == Subjects):
        if (r == "Subjects"):
            values.append(get_values_from_peewee_clause(Subjects.select().where(Subjects.Subject ** r_text), "Subject"))
        else:
            values.append(get_values_from_peewee_clause(Subjects.select().join(Subjects).where(Subjects.Subject ** r_text), "Subject"))

            # elif (c == Departments):
        if (r == "Departments"):
            values.append(get_values_from_peewee_clause(Departments.select().where(Departments.Dept ** r_text), "Dept"))
        else:
            values.append(get_values_from_peewee_clause(Departments.select().join(Departments).where(Departments.Dept ** r_text), "Dept"))


        print values
        values = [item for sublist in values for item in sublist]
        return jsonify({"values": values})
    else:
        abort(404)



@app.route('/api')
def api():
    q = request.args.get('q', 'engineering')
    # print q
    # if (" in " in q) or (" for " in q):
        # return redirect(url_for('query', q=q),307)
    # else:
    return redirect(url_for('search', q=q),307)

# if __name__ == '__main__':
#     app.run(debug = True, host='myfoot.org')
