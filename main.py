from flask import Flask, redirect, url_for, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def log():
    return render_template("login.html")

@app.route('/', methods = ['POST'])
def login():
    password = []
    user_name = request.form['username']
    password.append(request.form['password'])
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users where user=?",(user_name,))
    dpassword = c.fetchall()
    conn.close()
    print(dpassword[0])
    print(password)
    if dpassword == password:
        print("correct")
        return redirect(url_for('home'))
    else:
        print("failed")
        return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)