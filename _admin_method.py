from init import *


@app.route('/admin_index', methods=['GET', 'POST'])
def admin_index():
    global students, student_list
    if request.method == 'POST':
        button_edit = request.form.get('edit')
        button_delete = request.form.get('delete')
        if request.form.get('searchbtn') == 'searchbtn':
            class_to_check = request.form.get('class_to_check')
            sth_to_check = request.form.get('sth_to_check')
            if class_to_check == 'yxh':
                res = get_data('select * from student where yxh in (select yxh from department where mc like \'%' + sth_to_check + '%\')')
            else:
                res = get_data('select * from student where ' + class_to_check + ' like \'%' + sth_to_check + '%\'')
            setStudents([])
            students = varStudents()
            for s in res:
                xy = get_data('select mc from department where yxh=' + s[6])
                students.append((s[0], s[1], s[2], xy[0][0], s[5]))
            return render_template('admin_index.html', idents=students, indextype='student')
        elif button_edit:
            return redirect(url_for('edit', utype='student', info=button_edit))
        elif button_delete:
            try:
                delete_data('student', button_delete)
                return redirect('/admin_index')
            except pymssql.IntegrityError:
                render_template('admin_error.html')
        else:
            chklist = request.form.getlist('sub')
            delete_data('student', *chklist)
            return redirect('/admin_index')
    else:
        setStudentlist(get_data('select * from student'))
        student_list = varStudentlist()
        setStudents([])
        students = varStudents()
        for s in student_list:
            xy = get_data('select mc from department where yxh=' + s[6])
            students.append((s[0], s[1], s[2], xy[0][0], s[5]))
        return render_template('admin_index.html', idents=students, indextype='student')


@app.route('/admin_index_teacher', methods=['GET', 'POST'])
def admin_index_teacher():
    global teachers, teacher_list
    if request.method == 'POST':
        button_edit = request.form.get('edit')
        button_delete = request.form.get('delete')
        if request.form.get('searchbtn') == 'searchbtn':
            class_to_check = request.form.get('class_to_check')
            sth_to_check = request.form.get('sth_to_check')
            if class_to_check == 'yxh':
                res = get_data(
                    'select * from teacher where yxh in (select yxh from department where mc like \'%' + sth_to_check + '%\')')
            else:
                res = get_data('select * from teacher where ' + class_to_check + ' like \'%' + sth_to_check + '%\'')
            setTeachers([])
            teachers = varTeachers()
            for s in res:
                xy = get_data('select mc from department where yxh=' + s[6])
                teachers.append((s[0], s[1], s[2], xy[0][0], s[4]))
            return render_template('admin_index.html', idents=teachers, indextype='teacher')
        elif button_edit:
            return redirect(url_for('edit', utype='teacher', info=button_edit))
        elif button_delete:
            try:
                delete_data('teacher', button_delete)
                return redirect('/admin_index_teacher')
            except pymssql.IntegrityError:
                render_template('admin_error.html')
        else:
            chklist = request.form.getlist('sub')
            delete_data('teacher', *chklist)
            return redirect('/admin_index_teacher')
    else:
        setTeacherlist(get_data('select * from teacher'))
        teacher_list = varTeacherlist()
        setTeachers([])
        teachers = varTeachers()
        for s in teacher_list:
            xy = get_data('select mc from department where yxh=' + s[6])
            teachers.append((s[0], s[1], s[2], xy[0][0], s[4]))
        return render_template('admin_index.html', idents=teachers, indextype='teacher')


@app.route('/admin_index_course', methods=['GET', 'POST'])
def admin_index_course():
    global courses, course_list
    if request.method == 'POST':
        button_edit = request.form.get('edit')
        button_delete = request.form.get('delete')
        if request.form.get('searchbtn') == 'searchbtn':
            class_to_check = request.form.get('class_to_check')
            sth_to_check = request.form.get('sth_to_check')
            if class_to_check == 'km':
                res = get_data(
                    'select * from opencourse where kh in (select kh from course where km like \'%' + sth_to_check + '%\')')
            elif class_to_check == 'xm':
                res = get_data(
                    'select * from opencourse where gh in (select gh from teacher where xm like \'%' + sth_to_check + '%\')')
            else:
                res = get_data('select * from opencourse where ' + class_to_check + ' like \'%' + sth_to_check + '%\'')
            setCourses([])
            courses = varCourses()
            for s in res:
                km = get_data('select km from course where kh=' + s[1])
                tm = get_data('select xm from teacher where gh=' + s[2])
                courses.append((s[1], km[0][0], s[0], s[3], s[2], tm[0][0]))
            return render_template('admin_index.html', idents=courses, indextype='course')
        elif button_edit:
            info = button_edit.split()
            return redirect(url_for('edit', utype='opencourse', info=info))
        elif button_delete:
            info = button_delete.split()
            try:
                delete_data('course', info)
                return redirect('/admin_index_course')
            except pymssql.IntegrityError:
                render_template('admin_error.html')
        else:
            chklist = request.form.getlist('sub')
            for x in chklist[::]:
                chklist.remove(x)
                chklist.append(x.split())
            delete_data('course', *chklist)
            return redirect('/admin_index_course')
    else:
        setCourselist(get_data('select * from opencourse'))
        course_list = varCourselist()
        setCourses([])
        courses = varCourses()
        for s in course_list:
            km = get_data('select km from course where kh=' + s[1])
            tm = get_data('select xm from teacher where gh=' + s[2])
            courses.append((s[1], km[0][0], s[0], s[3], s[2], tm[0][0]))
        return render_template('admin_index.html', idents=courses, indextype='course')


@app.route('/admin_index_allcourse', methods=['GET', 'POST'])
def admin_index_allcourse():
    global courses, course_list
    if request.method == 'POST':
        button_edit = request.form.get('edit')
        button_delete = request.form.get('delete')
        if request.form.get('searchbtn') == 'searchbtn':
            class_to_check = request.form.get('class_to_check')
            sth_to_check = request.form.get('sth_to_check')
            if class_to_check == 'yxh':
                res = get_data(
                    'select * from course where yxh in (select yxh from department where mc like \'%' + sth_to_check + '%\')')
            else:
                res = get_data('select * from course where ' + class_to_check + ' like \'%' + sth_to_check + '%\'')
            setCourses([])
            courses = varCourses()
            for s in res:
                xy = get_data('select mc from department where yxh=' + s[4])
                courses.append((s[0], s[1], s[2], s[3], xy[0][0]))
            return render_template('admin_index.html', idents=courses, indextype='allcourse')
        elif button_edit:
            info = button_edit
            return redirect(url_for('edit', utype='course', info=info))
        elif button_delete:
            info = button_delete
            try:
                delete_data('allcourse', info)
                return redirect('/admin_index_allcourse')
            except pymssql.IntegrityError:
                return render_template('admin_error.html')
        else:
            chklist = request.form.getlist('sub')
            for x in chklist[::]:
                chklist.remove(x)
                chklist.append(x.split())
            delete_data('allcourse', *chklist)
            return redirect('/admin_index_allcourse')
    else:
        setCourselist(get_data('select * from course'))
        course_list = varCourselist()
        setCourses([])
        courses = varCourses()
        for s in course_list:
            xy = get_data('select mc from department where yxh=' + s[4])
            courses.append((s[0], s[1], s[2], s[3], xy[0][0], s[4]))
        return render_template('admin_index.html', idents=courses, indextype='allcourse')


@app.route('/add/<utype>', methods=['GET', 'POST'])
def add(utype):
    if request.method == 'GET':
        xy = get_data('select mc from department')
        return render_template('add.html', indextype=utype, allxy=xy)
    else:
        if utype == 'student':
            try:
                insert_data(utype, xh=request.form.get('xh'), xm=request.form.get('xm'),
                                  xb=request.form.get('xb'), csrq=request.form.get('csrq'),
                                  sjhm=request.form.get('sjhm'), xy=request.form.get('xy'), jg=request.form.get('jg'))
                return redirect('/admin_index')
            except pymssql.IntegrityError:
                render_template('admin_error.html')
        elif utype == 'teacher':
            try:
                insert_data(utype, gh=request.form.get('gh'), xm=request.form.get('xm'),
                                  xb=request.form.get('xb'), csrq=request.form.get('csrq'),
                                  jbgz=request.form.get('jbgz'), xy=request.form.get('xy'), xl=request.form.get('xl'))
                return redirect('/admin_index_teacher')
            except pymssql.IntegrityError:
                render_template('admin_error.html')
        elif utype == 'course':
            try:
                insert_data(utype, gh=request.form.get('gh'), kh=request.form.get('kh'),
                                  xq=request.form.get('xq'), sksj=request.form.get('sksj'), rl=request.form.get('rl'))
                return redirect('/admin_index_course')
            except pymssql.DatabaseError as e:
                m = e.args[1]
                n = m.decode('utf-8')
                p = n[:41] + n[79:89] + n[131:139]
                q = n[184:-1]
                return render_template('admin_error.html', info=p, detail=q)
        elif utype == 'allcourse':
            try:
                insert_data(utype, km=request.form.get('km'), kh=request.form.get('kh'),
                                  xf=request.form.get('xf'), xs=request.form.get('xs'), xy=request.form.get('xy'))
                return redirect('/admin_index_allcourse')
            except pymssql.IntegrityError:
                render_template('admin_error.html')


@app.route('/edit/<utype>+<info>', methods=['GET', 'POST'])
def edit(utype, info):
    if request.method == 'GET':
        if utype in ('student', 'teacher'):
            type_to_key = dict({'student': 'xh', 'teacher': 'gh'})
            temp = get_data('select * from ' + utype + ' where ' + type_to_key[utype] + '=\'' + info + '\'')[0]
            info = tuple(temp)
            info = [i.strip() if isinstance(i, str) else i for i in info]
            xy = get_data('select yxh,mc from department')
            for i in xy[::]:
                xy.remove(i)
                i = [j.strip() for j in i]
                xy.append(tuple(i))
            return render_template('edit.html', indextype=utype, indexinfo=info, allxy=xy, bexy=info[6])
        elif utype == 'opencourse':
            sql = 'select * from ' + utype + ' where kh=\'' + info[2:10] + '\' and gh=\'' + info[14:18] + '\' and xq=\'' + info[22:-2] + '\''
            print(sql)
            temp = get_data(sql)[0]
            info = tuple(temp)
            info = [i.strip() if isinstance(i, str) else i for i in info]
            return render_template('edit.html', indextype=utype, indexinfo=info)
        sql = 'select * from course where kh=\'' + info + '\''
        temp = get_data(sql)[0]
        info = tuple(temp)
        info = [i.strip() for i in info]
        xy = get_data('select yxh,mc from department')
        for i in xy[::]:
            xy.remove(i)
            i = [j.strip() for j in i]
            xy.append(tuple(i))
        return render_template('edit.html', indextype=utype, indexinfo=info, allxy=xy, bexy=info[4])
    else:
        if utype == 'student':
            edit_data(utype, xh=request.form.get('xh'), xb=request.form.get('xb'), csrq=request.form.get('csrq'),
                            sjhm=request.form.get('sjhm'), jg=request.form.get('jg'), yxh=request.form.get('xy'),
                            pwd=request.form.get('pwd'))
            return redirect('/admin_index')
        elif utype == 'teacher':
            edit_data(utype, gh=request.form.get('gh'), xb=request.form.get('xb'), csrq=request.form.get('csrq'),
                            jbgz=request.form.get('jbgz'), xl=request.form.get('xl'), yxh=request.form.get('xy'),
                            pwd=request.form.get('pwd'))
            return redirect('/admin_index_teacher')
        elif utype == 'opencourse':
            try:
                edit_data(utype, xq=request.form.get('xq'), kh=request.form.get('kh'), gh=request.form.get('gh'),
                                sksj=request.form.get('sksj'), rl=request.form.get('rl'))
                return redirect('/admin_index_course')
            except pymssql.DatabaseError as e:
                m = e.args[1]
                n = m.decode('utf-8')
                p = n[:41] + n[79:89] + n[131:139]
                q = n[184:-1]
                return render_template('admin_error.html', info=p, detail=q)
        elif utype == 'course':
            edit_data(utype, km=request.form.get('km'), kh=request.form.get('kh'), xf=request.form.get('xf'),
                            xs=request.form.get('xs'), yxh=request.form.get('xy'))
            return redirect('/admin_index_allcourse')


@app.route('/statistic/<utype>', methods=['GET', 'POST'])
def statistic(utype):
    if utype == 'student':
        tmp = get_data('select jg,avg(zpcj) from student,exam where student.xh=exam.xh group by jg')
        cat = [i[0].strip() for i in tmp]
        dat = [i[1] for i in tmp]
        dic = dict()
        for i in range(len(cat)):
            dic[cat[i]] = dat[i]
        return render_template('statistic.html', indextype=utype, dic=dic.items(), xl=cat, rs=dat)
    if utype == 'teacher':
        tmp = get_data('select xl,count(xl) from teacher group by xl')
        cat = [i[0].strip() for i in tmp]
        dat = [i[1] for i in tmp]
        dic = dict()
        for i in range(len(cat)):
            dic[cat[i]] = dat[i]
        return render_template('statistic.html', indextype=utype, dic=dic.items(), xl=cat, rs=dat)
    if utype == 'course':
        tmp = get_data(
            'select km,xq,AVG(zpcj) from exam,course where zpcj is not null and exam.kh=course.kh group by km,xq')
        km = [i[0].strip() for i in tmp]
        xq = [i[1].strip() for i in tmp]
        cj = [i[2] for i in tmp]
        dic = dict()
        for i in tmp:
            dic.setdefault(i[1].strip(), {})[i[0].strip()] = i[2]
        return render_template('statistic.html', indextype=utype, dic=xq, xl=km, rs=cj, info=tmp)
