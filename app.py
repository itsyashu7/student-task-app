from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect("database.db")
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


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")

    if username:
        session["username"] = username
        flash("Login successful")
        return redirect("/dashboard")

    flash("Login failed","error")
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    conn = get_db()
    tasks = conn.execute(
        "SELECT id, task, status FROM tasks WHERE username = ?",
        (session["username"],)
    ).fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        tasks=tasks
    )


@app.route("/add-task", methods=["POST"])
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


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
