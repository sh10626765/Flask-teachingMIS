import pymssql


def get_data(sqlquery):
    conn = pymssql.connect(server='127.0.0.1', user='sa', password='leevants', database='school')
    cur = conn.cursor()
    cur.execute(sqlquery)
    res = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return res


def insert_data(type, **value):
    conn = pymssql.connect(server='127.0.0.1', user='sa', password='leevants', database='school')
    cur =conn.cursor()
    sql = ''
    if type == 'student':
        yxh = get_data('select yxh from department where mc=\'' + value['xy'] + '\'')
        yxh = yxh[0][0]
        cur.callproc('dbo.insertStudent', (value['xh'], value['xm'], value['xb'], value['jg'], yxh, value['xh'], value['sjhm'], value['csrq']))
    elif type == 'teacher':
        yxh = get_data('select yxh from department where mc=\'' + value['xy'] + '\'')
        yxh = yxh[0][0]
        cur.callproc('dbo.insertTeacher', (value['gh'], value['xm'], value['xb'], value['xl'], value['jbgz'], yxh, value['gh'], value['csrq']))
    elif type == 'course':
        cur.callproc('dbo.insertOpencourse', (value['xq'], value['kh'], value['gh'], value['sksj'], value['rl']))
    elif type == 'allcourse':
        yxh = get_data('select yxh from department where mc=\'' + value['xy'] + '\'')
        yxh = yxh[0][0]
        cur.callproc('dbo.insertCourse', (value['kh'], value['km'], value['xf'], value['xs'], yxh))
    cur.close()
    conn.commit()
    conn.close()


def delete_data(type, *value):
    conn = pymssql.connect(server='127.0.0.1', user='sa', password='leevants', database='school')
    cur = conn.cursor()
    if type == 'student':
        for s in value:
            cur.execute('delete from student where xh=\'' + s + '\'')
    elif type == 'teacher':
        for s in value:
            cur.execute('delete from teacher where gh=\'' + s + '\'')
    elif type == 'course':
        for s in value:
            cur.execute('delete from opencourse where kh=\'' + s[0] + '\' and gh=\'' + s[1] + '\' and xq=\'' + s[2] + '\'')
    elif type == 'allcourse':
        for s in value:
            cur.execute('delete from course where kh=\'' + s + '\'')
    cur.close()
    conn.commit()
    conn.close()


def edit_data(type, **value):
    conn = pymssql.connect(server='127.0.0.1', user='sa', password='leevants', database='school')
    cur = conn.cursor()
    if type == 'student':
        cur.callproc('dbo.updateStudent',
                     (value['xh'], value['xb'], value['jg'], value['yxh'], value['pwd'], value['sjhm'], value['csrq']))
    elif type == 'teacher':
        cur.callproc('dbo.updateTeacher',
                     (value['gh'], value['xb'], value['xl'], value['jbgz'], value['yxh'], value['pwd'], value['csrq']))
    elif type == 'opencourse':
        cur.callproc('dbo.updateOpencourse', (value['xq'], value['kh'], value['gh'], value['sksj'], value['rl']))
    elif type == 'course':
        cur.callproc('dbo.updateCourse', (value['kh'], value['km'], value['xf'], value['xs'], value['yxh']))
    cur.close()
    conn.commit()
    conn.close()


def change_table_data(sqlquery):
    conn = pymssql.connect(server='127.0.0.1', database='school')
    cur = conn.cursor()
    cur.execute(sqlquery)
    cur.close()
    conn.commit()
    conn.close()