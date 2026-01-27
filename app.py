from flask import Flask, render_template,request,redirect,session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login" , methods=["GET","POST"])
def login():
    username = request.form.get("username")
    if username:
        session["username"] = username
        return redirect("/dashboard")
    
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    conn = get_db()
    tasks = conn.execute("SELECT task FROM tasks WHERE username = ?",(session["username"],)).fetchall()
    conn.close()

    return render_template("dashboard.html",username = session["username"],tasks = tasks)

@app.route("/add-task", methods=["POST"])
def add_task(): 
    if "username" not in session:
        return redirect("/")
    
    task = request.form.get("task")
    username = session["username"]

    if task:
        conn = get_db()
        conn.execute("INSERT INTO tasks(username,task)VALUES(?,?)",(username,task))
        conn.commit()
        conn.close()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = sqlite3.connect("database.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,task TASK)""")
    conn.commit()
    conn.close()
create_table()

if __name__== "__main__":
    app.run(debug=True)