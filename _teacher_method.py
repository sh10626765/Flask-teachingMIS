from init import *


@app.route('/teacher_change_grade', methods=['GET', 'POST'])
def teacher_change_grade():
    global stugra_info
    data = varData()
    if request.method=='GET':                    #点击修改学生信息后跳至    输入成绩页面

        grades_info = varGradeInfo()
        return render_template('teacher_change_grade.html',ident='教师',
                           name=data[0][1].strip(), courses=stugra_info)
    if request.method == 'POST':
        s_no = request.form.get('stuno')
        pscj = request.form.get('ps_grade')
        kscj = request.form.get('ks_grade')
        sqlquery = 'update exam set pscj='+ pscj +' where (xh= '+ s_no + ' and gh='+data[0][0]+' and kh='+ ccno + ')'
        change_pscj=change_table_data(sqlquery)
        sqlquery = 'update exam set kscj=' + kscj + ' where (xh= ' + s_no + ' and gh=' + data[0][0] + ' and kh=' + ccno + ')'
        change_kscj = change_table_data(sqlquery)
        sqlquery = 'select * from exam where gh=' + data[0][0] + ' and kh=' + ccno
        opencourse = get_data(sqlquery)
        stugra_info = []
        for grade in opencourse:
            xh = grade[0]
            c_sname = get_data('select xm from student where xh=' + xh)
            sxm = c_sname[0][0]
            pscj = grade[4]
            kscj = grade[5]
            zpcj = grade[6]
            stugra_info.append((xh, sxm, pscj, kscj, zpcj))

        return render_template('teacher_change_grade.html',ident='教师',
                           name=data[0][1].strip(), courses=stugra_info)


@app.route('/teacher_index', methods=['GET', 'POST'])
def teacher_index():
    global stugra_info
    global ccno
    data = varData()
    if request.method=='GET':
        return render_template('teacher_check.html', ident='教师',
                               name=data[0][1].strip())
    if request.method == 'POST':                                  #点击查询 显示学生的成绩信息
        ccno = request.form.get('courseno') + '  '
        lesson_open_by_teacher = varLessonOpenByTeacher()
        if ccno in lesson_open_by_teacher:
            sqlquery = 'select * from exam where gh=' + data[0][0] + ' and kh=' + ccno +' and xq=\'2012-2013冬季\''
            opencourse = get_data(sqlquery)
            if opencourse==[]:
                return render_template('teacher_check.html', name=data[0][1].strip(), ident='教师', wrongtype='notthisterm')
            else:
                sqlquery = 'select * from exam where gh=' + data[0][0] + ' and kh=' + ccno
                opencourse = get_data(sqlquery)
                setStugraInfo([])
                stugra_info = varStugraInfo()
                for grade in opencourse:
                    xh = grade[0]
                    c_sname = get_data('select xm from student where xh=' + xh)
                    sxm = c_sname[0][0]
                    pscj = grade[4]
                    kscj = grade[5]
                    zpcj = grade[6]
                    stugra_info.append((xh, sxm, pscj, kscj, zpcj))

                return render_template('teacher_check.html', ident='教师',
                                       name=data[0][1].strip(), courses=stugra_info)
        else:
            return render_template('teacher_check.html', name=data[0][1].strip(), ident='教师', wrongtype='notopen')

