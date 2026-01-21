from flask import Flask, render_template, url_for,request,redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login" , methods=["GET","POST"])
def login():
    username = request.form.get("username")
    return render_template("dashboard.html",username=username)
    return redirect("/")

if __name__== "__main__":
    app.run(debug=True)