from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect("database.db",timeout=10,check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            task TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


create_table()


def create_users_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password TEXT)""")
    conn.commit()
    conn.close()

create_users_table()


def login_required(f):
    @wraps(f)
    def decorated_function(*args,  **kwargs):
        if "username" not in session:
            flash("Please login first", "error")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# ---------- ROUTES ----------
@app.route("/")
def home():
    return redirect("/register")


@app.route("/login", methods=["GET" , "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect("/register") 

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?",(username,)).fetchone()
    conn.close()

    if user and check_password_hash(user["password"],password):
        session["username"] = username
        flash("Login Successful","success")
        return redirect("/dashboard")
    
    flash("Invalid username or password","error")
    return redirect("/login")


@app.route("/dashboard")
@login_required
def dashboard():
    if "username" not in session:
        return redirect("/")

    conn = get_db()
    tasks = conn.execute(
        "SELECT id, task, status FROM tasks WHERE username = ?",
        (session["username"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", username=session["username"],tasks=tasks)


@app.route("/add-task", methods=["POST"])
@login_required
def add_task():
    if "username" not in session:
        return redirect("/")

    task = request.form.get("task")

    if task:
        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (username, task, status) VALUES (?, ?, 'pending')",
            (session["username"], task)
        )
        conn.commit()
        conn.close()
        flash("Task added successfully","success")

    return redirect("/dashboard")


@app.route("/delete-task/<int:task_id>")
@login_required
def delete_task(task_id):
    if "username" not in session:
        return redirect("/")

    conn = get_db()
    conn.execute(
        "DELETE FROM tasks WHERE id = ? AND username = ?",
        (task_id, session["username"])
    )
    conn.commit()
    conn.close()

    flash("Task deleted","success")
    return redirect("/dashboard")


@app.route("/toggle-task/<int:task_id>")
@login_required
def toggle_task(task_id):
    if "username" not in session:
        return redirect("/")

    conn = get_db()
    task = conn.execute(
        "SELECT status FROM tasks WHERE id = ? AND username = ?",
        (task_id, session["username"])
    ).fetchone()

    if task is None:
        conn.close()
        flash("Task not found","error")
        return redirect("/dashboard")

    new_status = "completed" if task["status"] == "pending" else "pending"

    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ? AND username = ?",
        (new_status, task_id, session["username"])
    )
    conn.commit()
    conn.close()

    flash("Task status updated","info")
    return redirect("/dashboard")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("All fields are required", "error")

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute("INSERT INTO users (username,password) VALUES (?, ?)",(username, hashed_password))
            conn.commit()
            conn.close()
            flash("Account created successfully","success")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Username already exists","error")
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
