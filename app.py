from flask import Flask, render_template, redirect, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "629102"

def db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREATE USERS TABLE
conn = db()
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT,
password TEXT,
pin TEXT
)
""")
conn.commit()

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["Rakesh"]
        p = request.form["Rakesh999"]

        user = db().execute("SELECT * FROM users WHERE username=? AND password=?", (u,p)).fetchone()

        if user:
            session["user"] = u
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/users", methods=["GET","POST"])
def users():
    conn = db()

    if request.method == "POST":
        conn.execute("INSERT INTO users (username,password,pin) VALUES (?,?,?)",
                     (request.form["username"], request.form["password"], request.form["pin"]))
        conn.commit()

    data = conn.execute("SELECT * FROM users").fetchall()
    return render_template("users.html", users=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
def home():
    return "Admin Panel Running"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
