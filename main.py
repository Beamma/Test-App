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
    if logstatus == "true" and xadmin == "Admin":
        return render_template("home.html", admin = "Admin")
    if logstatus == "true" and xadmin != "Admin":
        return render_template("home.html")
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
