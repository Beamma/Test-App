from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()

@app.route('/')
def log():
    return render_template("login.html")

@app.route('/', methods = ['POST'])
def login():
    session['logstatus'] = 'false'
    user_name = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users where user=?",(user_name,))
    for i in c.fetchall():
        for j in i:
            dpassword = j
    conn.close()
    print(dpassword)
    print(password)
    if dpassword == password:
        print("correct")
        session['logstatus'] = 'true'
        return redirect(url_for('home'))
    else:
        print("failed")
        return render_template("login.html")

@app.route('/home')
def home():
    logstatus = 'false'
    logstatus = session.get('logstatus', None)
    if logstatus == "true":
        return render_template("home.html")
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
