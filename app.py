#host='wangtong-mysql'
from flask import Flask, request, render_template
import mysql.connector
app = Flask(__name__)

@app.route('/', methods=['GET'])
def signin_form():
    return render_template('admin/index.html')   

@app.route('/check', methods=['POST'])
def check():
    id = request.form['id']
    title =request.form['title']
    digest=request.form['digest']
    content=request.form['content']
    return render_template('admin/information.html',id=id,title=title,digest=digest,content=content) 

@app.route('/check_tec', methods=['POST'])
def check_tec():
    username=request.form['username']
    id = request.form['id']
    title =request.form['title']
    digest=request.form['digest']
    content=request.form['content']
    return render_template('admin/news_review_detail.html',username=username,id=id,title=title,digest=digest,content=content)    

@app.route('/login_stu', methods=['GET'])
def login_stu():
    return render_template('admin/login_stu.html') 

@app.route('/login_tec', methods=['GET'])
def login_tec():
    return render_template('admin/login_tec.html')

@app.route('/login_stu', methods=['POST'])
def signin_stu():
    username = request.form['username']
    password = request.form['password']
    conn = mysql.connector.connect(host='wangtong-mysql',user='root', password='Aaa',database='test')
    cursor_pwd = conn.cursor()
    sql_pwd='select password from stu where id=%s'
    cursor_pwd.execute(sql_pwd,[username])
    result_pwd = cursor_pwd.fetchall()

    cursor_digest = conn.cursor()
    sql_digest='select digest from program where id=%s'
    cursor_digest.execute(sql_digest,[username])
    result_digest = cursor_digest.fetchall()

    cursor_content = conn.cursor()
    sql_content='select content from program where id=%s'
    cursor_content.execute(sql_content,[username])
    result_content = cursor_content.fetchall()

    cursor_title = conn.cursor()
    sql_title='select title from program where id=%s'
    cursor_title.execute(sql_title,[username])
    result_title = cursor_title.fetchall()
    if(result_title):
        count=1
    else:count=0
    
    cursor_sta = conn.cursor()
    sql_sta='select status from program where id=%s'
    cursor_sta.execute(sql_sta,[username])
    result_sta = cursor_sta.fetchall()

    if result_pwd and result_pwd[0][0] == password:
        if result_title and result_content and result_digest:
            return render_template('admin/news_edit.html', status=result_sta[0][0],id=username,count=count,title=result_title[0][0],digest=result_digest[0][0],content=result_content[0][0])
        else:return render_template('admin/news_edit.html', id=username,count=count)
    return render_template('admin/login_stu.html', message='Bad username or password', username=username)

@app.route('/login_tec', methods=['POST'])
def signin_tec():
    username = request.form['username']
    password = request.form['password']
    conn = mysql.connector.connect(host='wangtong-mysql',user='root', password='Aaa',database='test')
    cursor = conn.cursor()
    sql='select password from tec where id=%s'
    cursor.execute(sql,[username])
    result = cursor.fetchall()

    cursor_count = conn.cursor()
    sql_count='select count(*) from program'
    cursor_count.execute(sql_count)
    result_count = cursor_count.fetchall()
    count=result_count[0][0]

    cursor_id = conn.cursor()
    sql_id='select id from program'
    cursor_id.execute(sql_id)
    result_id = cursor_id.fetchall()

    cursor_title = conn.cursor()
    sql_title='select title from program'
    cursor_title.execute(sql_title)
    result_title = cursor_title.fetchall()

    cursor_digest = conn.cursor()
    sql_digest='select digest from program'
    cursor_digest.execute(sql_digest)
    result_digest = cursor_digest.fetchall()

    cursor_content = conn.cursor()
    sql_content='select content from program'
    cursor_content.execute(sql_content)
    result_content = cursor_content.fetchall()

    cursor_sta = conn.cursor()
    sql_sta='select status from program'
    cursor_sta.execute(sql_sta)
    result_sta = cursor_sta.fetchall()

    a=[]
    for i in range(count):
        a.append(result_id[i][0])
    
    b=[]
    for i in range(count):
        b.append(result_title[i][0])

    c=[]
    for i in range(count):
        c.append(result_digest[i][0])

    d=[]
    for i in range(count):
        d.append(result_content[i][0])

    e=[]
    for i in range(count):
        e.append(result_sta[i][0])
    
    if result and result[0][0] == password:
        return render_template('admin/news_review.html', username=username,count=count,id=a,title=b,digest=c,content=d,status=e)
    return render_template('admin/login_tec.html', message='Bad username or password', username=username)

@app.route('/pwd_edit_stu', methods=['GET'])
def pwd_edit_stu():
    return render_template('admin/pwd_edit_stu.html') 

@app.route('/pwd_edit_tec', methods=['GET'])
def pwd_edit_tec():
    return render_template('admin/pwd_edit_tec.html')     

@app.route('/pwd_edit_stu', methods=['POST'])
def edit_post_stu():
    id=request.form['id']
    old=request.form['old']
    new = request.form['new']
    new_confirm = request.form['new_confirm']
    conn = mysql.connector.connect(host='wangtong-mysql',user='root', password='Aaa',database='test')

    cursor_old = conn.cursor()
    sql='select password from stu where id=%s'
    cursor_old.execute(sql,[id])
    result_old = cursor_old.fetchall()

    if result_old and result_old[0][0] == old and new==new_confirm:
        cursor = conn.cursor()
        cursor.execute('update stu set password=%s where id=%s',(new,id))
        cursor.rowcount
        conn.commit()
        cursor.close()
        return render_template('admin/edit_ok.html')
    return render_template('admin/pwd_edit_stu.html',message='Bad username or password',) 

@app.route('/pwd_edit_tec', methods=['POST'])
def edit_post_tec():
    id=request.form['id']
    old=request.form['old']
    new = request.form['new']
    new_confirm = request.form['new_confirm']
    conn = mysql.connector.connect(host='wangtong-mysql',user='root', password='Aaa',database='test')

    cursor_old = conn.cursor()
    sql='select password from tec where id=%s'
    cursor_old.execute(sql,[id])
    result_old = cursor_old.fetchall()

    if result_old and result_old[0][0] == old and new==new_confirm:
        cursor = conn.cursor()
        cursor.execute('update tec set password=%s where id=%s',(new,id))
        cursor.rowcount
        conn.commit()
        cursor.close()
        return render_template('admin/edit_ok.html')
    return render_template('admin/pwd_edit_tec.html',message='Bad username or password',) 

@app.route('/edit_ok', methods=['GET'])
def edit_ok():
    return render_template('admin/edit_ok.html')   

@app.route('/news_edit', methods=['POST'])
def news_edit_form():
    id=request.form['id']
    return render_template('admin/news_edit_detail.html',id=id)

@app.route('/news_edit_detail', methods=['POST'])
def news_edit_detail():
    id=request.form['id']
    title = request.form['title']
    digest = request.form['digest']
    content = request.form['content']
    a=content.replace("&nbsp;","")
    b=a.replace("<p>","")
    c=b.replace("</p>","") 
    conn = mysql.connector.connect(host='wangtong-mysql',user='root', password='Aaa', database='test')
    cursor = conn.cursor()
    cursor.execute('delete from program where id=%s',[id])
    cursor.execute('insert into program (id,title, digest,content) values (%s,%s, %s,%s)', (id,title,digest,c))
    cursor.rowcount
    conn.commit()
    cursor.close()
    cursor_title = conn.cursor()
    sql_title='select title from program where id=%s'
    cursor_title.execute(sql_title,[id])
    result_title = cursor_title.fetchall()
    if(result_title):
        count=1
    else:count=0
    return render_template('admin/news_edit.html',count=count,id=id,title=title,digest=digest,content=c)

@app.route('/news_review_detail', methods=['POST'])
def news_review_detail_form():
    username=request.form['username']
    id=request.form['id']
    sta = request.form['action']
    if sta == "accept":status=1
    else:status=0
    conn = mysql.connector.connect(host='wangtong-mysql',user='root', password='Aaa', database='test')
    cursor = conn.cursor()
    cursor.execute('update program set status=%s where id=%s',(status,id))
    cursor.rowcount
    conn.commit()
    cursor.close()
    
    cursor_count = conn.cursor()
    sql_count='select count(*) from program'
    cursor_count.execute(sql_count)
    result_count = cursor_count.fetchall()
    count=result_count[0][0]

    cursor_id = conn.cursor()
    sql_id='select id from program'
    cursor_id.execute(sql_id)
    result_id = cursor_id.fetchall()

    cursor_title = conn.cursor()
    sql_title='select title from program'
    cursor_title.execute(sql_title)
    result_title = cursor_title.fetchall()

    cursor_digest = conn.cursor()
    sql_digest='select digest from program'
    cursor_digest.execute(sql_digest)
    result_digest = cursor_digest.fetchall()

    cursor_content = conn.cursor()
    sql_content='select content from program'
    cursor_content.execute(sql_content)
    result_content = cursor_content.fetchall()

    cursor_sta = conn.cursor()
    sql_sta='select status from program'
    cursor_sta.execute(sql_sta)
    result_sta = cursor_sta.fetchall()

    a=[]
    for i in range(count):
        a.append(result_id[i][0])
    
    b=[]
    for i in range(count):
        b.append(result_title[i][0])

    c=[]
    for i in range(count):
        c.append(result_digest[i][0])

    d=[]
    for i in range(count):
        d.append(result_content[i][0])
    
    e=[]
    for i in range(count):
        e.append(result_sta[i][0])


    return render_template('admin/news_review.html',username=username,count=count,id=a,title=b,digest=c,content=d,status=e)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
