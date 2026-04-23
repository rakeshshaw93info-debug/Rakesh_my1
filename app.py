from flask import Flask, render_template, redirect, request, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "629102"

# ================= DATABASE =================
def db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = db()

# USERS TABLE
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password TEXT,
pin TEXT
)
""")

# CREATE DEFAULT ADMIN
conn.execute("""
INSERT OR IGNORE INTO users (id, username, password, pin)
VALUES (1, 'admin', 'admin123', '1111')
""")

conn.commit()

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        user = db().execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()

        if user:
            session["user"] = u
            return redirect("/dashboard")
        else:
            return "❌ Login Failed"

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

# ================= USERS =================
@app.route("/users", methods=["GET", "POST"])
def users():
    if "user" not in session:
        return redirect("/login")

    conn = db()

    if request.method == "POST":
        conn.execute("""
        INSERT INTO users (username, password, pin)
        VALUES (?, ?, ?)
        """, (
            request.form["username"],
            request.form["password"],
            request.form["pin"]
        ))
        conn.commit()

    data = conn.execute("SELECT * FROM users").fetchall()
    return render_template("users.html", users=data)

# ================= DELETE USER =================
@app.route("/delete_user/<int:id>")
def delete_user(id):
    conn = db()
    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    return redirect("/users")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= HOME =================
@app.route("/")
def home():
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
