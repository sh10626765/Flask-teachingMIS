from _admin_method import *
from _student_method import *
from _teacher_method import *


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', alert=0)
    else:
        user_type = request.form.get('ident')
        user = request.form.get('username')
        if user == '':
            user = 'null'
        pwd = request.form.get('password')
        if pwd == '':
            pwd = 'null'
        # print('user is %s %s, password is %s' % (user_type, user, pwd))
        user_type_to_id = {'student': 'xh', 'teacher': 'gh', 'adminn': 'uid'}
        sqlquery = 'select * from ' + user_type +\
                   ' where ' + user_type_to_id.get(user_type) + '=\'' + user +\
                   '\' and pwd=\'' + pwd + '\''
        setData(get_data(sqlquery))
        data = varData()
        if not data:
            return render_template('login.html', alert=1)

        if user_type == 'student':
            return redirect(url_for('student_index', user=user))
        elif user_type == 'adminn':
            return redirect('/admin_index')
        elif user_type == 'teacher':
            sqlquery = 'select * from opencourse where gh=' + user + ' order by xq desc'
            opencourse = get_data(sqlquery)
            setGradeInfo([])
            grades_info = varGradeInfo()
            setLessonOpenByTeacher([])
            lesson_open_by_teacher = varLessonOpenByTeacher()
            for course in opencourse:
                kh = course[1]
                getkm = get_data('select km from course where kh=' + kh)
                km = getkm[0][0]
                xq = course[0]
                '''xh = grade[0]
                c_sname = get_table_data('select xm from student where xh=' + xh)
                sxm = c_sname[0][0]
                c_gra = grade[5]
                c_term = grade[1]'''
                lesson_open_by_teacher.append(kh)
                grades_info.append((kh, km,xq))
            return render_template('teacher_index.html', ident='教师',
                                   name=data[0][1].strip(), courses=grades_info)





if __name__ == '__main__':
    app.run()
