from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()

@app.route('/')
def log():
    session['logstatus'] = 'false'
    return render_template("login.html")

@app.route('/', methods = ['POST'])
def login():
    admin = ''
    dpassword = ''
    session['logstatus'] = 'false'
    user_name = request.form['username']
    session['user'] = user_name
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users where user=?",(user_name,))
    for i in c.fetchall():
        for j in i:
            dpassword = j
    c.execute("SELECT admin From users where user=?",(user_name,))
    for i in c.fetchall():
        for q in i:
            admin = q
    print(admin)
    conn.close()
    session['xadmin'] = admin
    if dpassword == password:
        session['logstatus'] = 'true'
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route('/home')
def home():
    logstatus = 'false'
    xadmin = session.get('xadmin', None)
    logstatus = session.get('logstatus', None)
    users = []
    if logstatus == "true":
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT name, post, title FROM notices")
        posts = c.fetchall()
        conn.close()
        if xadmin == "Admin":
            return render_template("home.html", admin = "Admin", posts = posts)
        else:
            return render_template("home.html", admin = "False", posts = posts)
    else:
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    logstatus = 'false'
    xadmin = session.get('xadmin', None)
    logstatus = session.get('logstatus', None)
    if logstatus == "true" and xadmin == "Admin":
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT name, post, title FROM notices")
        posts = c.fetchall()
        conn.close()
        return render_template("admin.html", posts = posts)
    if logstatus == "true" and xadmin != "Admin":
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/admin', methods = ['POST'])
def post_admin():
    post_db = []
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    user_id = session.get('user', None)
    c.execute("SELECT name FROM users WHERE user=?", (user_id,))
    for i in c.fetchall():
        for j in i:
            name = j
    conn.close()
    post_db.insert(1, user_id)
    post_db.insert(2, request.form['post'])
    post_db.insert(3, name)
    post_db.insert(4, request.form['title'])
    sql = "INSERT INTO notices(user, post, name, title) VALUES(?,?,?,?)"
    val = post_db
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(sql, val)
    conn.commit()
    conn.close()
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(debug=True)
