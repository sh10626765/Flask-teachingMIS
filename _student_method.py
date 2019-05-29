from init import *


@app.route('/student_index/<user>', methods=['GET', 'POST'])
def student_index(user):
    global courses, name, avg_gpa
    name = get_data('select xm from student where xh=' + user)[0][0]
    if request.method == 'GET':
        setCourses(get_data('select * from exam where xh=' + user))
        courses = varCourses()  # 登录学生的选课记录
        gpalist = [(computeGPA(course[5]), course[2]) for course in courses]

        sum_gpa = 0
        sum_credit = 0
        for g in gpalist:  # 计算均绩
            if g[0] == 'nul':
                continue
            else:
                credit = int(get_data('select xf from course where kh=' + g[1])[0][0])
                sum_credit += credit
                sum_gpa += credit * g[0]
        avg_gpa = 1.0 * sum_gpa / sum_credit

        return render_template('student_index.html', indextype='main', ident='学生', gpa=avg_gpa, name=name.strip(),
                               user=user)


@app.route('/student_course/<user>', methods=['GET', 'POST'])
def student_course(user):
    global course_list, avg_gpa
    setCourselist(get_data('exec getStudentCourses @xh=' + user))
    course_list = varCourselist()
    print(course_list)
    xq = request.form.get('chxq')
    print(xq)

    if xq and xq != '选择学期' and request.method == 'POST':
        cl = [i for i in course_list if i[0].strip() == xq]
        return render_template('student_index.html', indextype='course_table', course_table=course_list, cl=cl, ident='学生',
                           gpa=avg_gpa, name=name.strip(), user=user)
    else:
        cl = course_list
        return render_template('student_index.html', indextype='course_table', course_table=course_list, cl=cl, ident='学生',
                           gpa=avg_gpa, name=name.strip(), user=user)


@app.route('/student_set/<user>', methods=['GET', 'POST'])
def student_set(user):
#选课退课
    name = get_data('select xm from student where xh=' + user)[0][0]
    if request.method == 'POST':
        if '选 课' in request.form.values():
            ccno = request.form.get('courseno')
            ttno = request.form.get('teacherno')
            cctime = request.form.get('coursetime')
            sqlquery = 'select * from exam where xh=' + user
            ccourse = get_data(sqlquery)

            for c in ccourse:
                if ccno == c[2].strip() and ttno == c[3].strip() and cctime == c[1].strip():
                    return render_template('tt.html', ident='学生',
                           name=name.strip(), courses=varCourselist(), gpa=avg_gpa, user=user) #历史课程不能选

            ocflag=0
            sqlquery1='select * from opencourse'
            oc=get_data(sqlquery1)
            for o in oc:
                if ccno == o[1].strip() and ttno == o[2].strip() and cctime == o[0].strip():
                    ocflag=1
            if ocflag==0:
                    return render_template('notexistclass.html', ident='学生',
                           name=name.strip(), courses=varCourselist(), gpa=avg_gpa, user=user) #不存在课程不能选
            else:
                # 数据库连接改一下
                conn = pymssql.connect(server='127.0.0.1', user='sa', password='leevants', database='school')
                cur = conn.cursor()
                print(user, cctime, ccno, ttno, 'NULL', 'NULL', 'NULL')
                sqlquery = 'select * from teacher where gh=' + ttno
                ttname_l = get_data(sqlquery)
                ttname = ''
                for t_e in ttname_l:
                    ttname = t_e[1]
                sqlquery = 'select * from course where kh=' + ccno
                ccname_l = get_data(sqlquery)
                ccname = ''
                for c_e in ccname_l:
                    ccname = c_e[1]
                courses_info.append((ccno, ccname, ttname, cctime, None, ttno))
                # 这里在exam表中增加当前选的课程
                cur.callproc('insertExam',(user, cctime, ccno, ttno, None, None, None))
                cur.close()
                conn.commit()
                conn.close()
            return redirect(url_for('student_set', user=user))


        elif '退 课' in request.form.values():
            ccno = request.form.get('courseno')
            ttno = request.form.get('teacherno')
            cctime = request.form.get('coursetime')
            ttname = request.form.get('teachername')
            sqlquery = 'select * from exam where xh=' + user
            ccourse = get_data(sqlquery)
            for c in ccourse:
                if ccno == c[2].strip() and ttno == c[3].strip() and cctime == c[1].strip() and c[6] != None:
                    return render_template('ttt.html', ident='学生',
                           name=name.strip(), gpa=avg_gpa, courses=varCourselist(), user=user)  # 已登分课程不能退
            ocflag = 0
            sqlquery1 = 'select * from opencourse'
            oc = get_data(sqlquery1)
            for o in oc:
                if ccno == o[1].strip() and ttno == o[2].strip() and cctime == o[0].strip():
                    ocflag = 1
            if ocflag == 0:
                return render_template('notexistclass.html', ident='学生',
                                           name=name.strip(), gpa=avg_gpa, courses=varCourselist(), user=user)  # 不存在课程不能退

            else:
                # 数据库连接改一下
                conn = pymssql.connect(server='127.0.0.1', user='sa', password='leevants', database='school')
                cur = conn.cursor()
                #这里删除当前输入的课程，未成功
                si='delete from exam where xq=\'' + cctime + '\' and kh=\'' + ccno + '\' and gh=\'' + ttno +'\' and xh=\'' + user + '\''
                try:
                    cur.execute(si)
                    cur.close()
                    conn.commit()
                except:
                    conn.rollback()
                conn.close()
                courses = varCourselist()
                print(courses)

            return redirect(url_for('student_set', user=user))


    setCourselist(get_data('exec getStudentCourses @xh=' + user))
    return render_template('student_set.html', ident='学生',
                           name=name.strip(), courses=varCourselist(), gpa=avg_gpa, user=user)


@app.route('/inqcourse', methods=['GET', 'POST'])
def inqcourse():
    slc_info=[]
    if request.method == 'POST':

        sltime = request.form.get('inqtime')
        sqlquery = 'select * from opencourse where xq= \''+sltime+'\''
        slcourse = get_data(sqlquery)

        slc_info = []
        for sc in slcourse:
            cno = sc[1]
            c_name = get_data('select km from course where kh=' + cno)
            c_name = c_name[0][0]
            c_tno = sc[2]
            c_tname = get_data('select xm from teacher where gh=' + c_tno)
            c_tname = c_tname[0][0]
            c_time = sc[3]
            c_term = sc[0]
            slc_info.append((cno, c_name, c_tno, c_tname, c_term, c_time))
        print(slc_info)
        print('x')
        return render_template('inqcourse.html', ident='学生',
                                   name=data[0][1].strip(),selected_course=slc_info)
    return render_template('inqcourse.html', ident='学生',
                           name=data[0][1].strip(), selected_course=slc_info)



ranktemp = get_data('select xh,avg(zpcj) from exam group by xh')  # 所有学生的平均成绩
setRanklist([])
ranklist = varRanklist()
for i in ranktemp:
    xh = i[0].strip()
    xm = get_data('select xm from student where xh=' + xh)
    ranklist.append((xm[0][0], i[1]))
ranklist = sorted(ranklist, key=lambda x: x[1], reverse=True)  # 根据学生平均成绩，对学生排名