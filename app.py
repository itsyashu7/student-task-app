from flask import Flask, render_template, request, redirect, session, flash,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from  itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail,Message
from dotenv import load_dotenv
import sqlite3,re,os,threading

app = Flask(__name__)
load_dotenv()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("EMAIL_USER")
app.config['MAIL_TIMEOUT'] = 20


mail = Mail(app)
app.secret_key = "supersecretkey"
serializer = URLSafeTimedSerializer(app.secret_key)


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




def create_users_table():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,email TEXT UNIQUE,password TEXT)""")
    conn.commit()
    conn.close()

create_table()
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

@app.route("/forgot-password", methods=["GET","POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email").strip().lower()

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?",(email,)).fetchone()
        conn.close()
        if user:
            token = serializer.dumps(email,salt="password-reset-salt")
            reset_url = url_for("reset_password",token=token, _external=True)
            msg = Message(subject="Reset Your Password",recipients=[email])
            msg.html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
            body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
            }}
            .container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            max-width: 500px;
            margin: auto;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}
            .btn {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #2563eb;
            color: white !important;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 15px;
            }}
            .footer {{
            font-size: 12px;
            color: #888;
            margin-top: 20px;
            }}
            </style>
            </head>
            <body>
            <div class="container">
            <h2>Password Reset Request</h2>
            <p>Hello,</p>
            <p>You requested to reset your password.</p>
            <p>Click the button below to reset it:</p>
            <a href="{reset_url}" class="btn">Reset Password</a>
            <p>This link will expire in 10 minutes.</p>                                                                                                                                                                                                                                                                                                                                                            
            <div class="footer">
            If you did not request this, please ignore this email.
            </div>
            </div>
            </body>
            </html>"""
            
            threading.Thread(target=send_async_email,args=(app,msg)).start()
            
            
        else:
            flash("email not found","error")
    return render_template("forgot_password.html")
def send_async_email(app,msg):
                with app.app_context():
                    try:
                        mail.send(msg)
                        flash("reset link sent check your email","success")
                    except Exception as e:
                        print("Email error:",e)

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(
            token,
            salt="password-reset-salt",
            max_age=600  # 10 minutes
        )
    except:
        flash("Reset link expired or invalid", "error")
        return redirect("/login")

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(request.url)

        hashed_password = generate_password_hash(password)

        conn = get_db()
        conn.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (hashed_password, email)
        )
        conn.commit()
        conn.close()

        flash("Password updated successfully", "success")
        return redirect("/login")

    return render_template("reset_password.html")

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
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        if not username or not password or not email or not confirmpassword:
            flash("All fields are required", "error")
        
        if  password!=confirmpassword:
            flash("Passwords do not match","error")
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"

        if not re.match(pattern, password):
            flash("Password must contain 8 characters,1 uppercase,1 lowercase,1 number and special character","error")
        
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute("INSERT INTO users (username,email,password) VALUES (?, ?, ?)",(username,email, hashed_password))
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
    app.run()
