from flask import Flask, request, render_template_string
import sqlite3, os

app = Flask(__name__)

def db():
    return sqlite3.connect("data.db")

# create table
conn = db()
conn.execute("""CREATE TABLE IF NOT EXISTS data (
id INTEGER PRIMARY KEY,
com TEXT,
brand TEXT,
mrp TEXT
)""")
conn.commit()

# home
@app.route("/")
def home():
    return """
    <h2>Admin Panel</h2>
    <form method='POST' action='/add'>
    COM:<input name='com'><br>
    BRAND:<input name='brand'><br>
    MRP:<input name='mrp'><br>
    <button>Add</button>
    </form>
    <br><a href='/view'>View Data</a>
    """

# add data
@app.route("/add", methods=["POST"])
def add():
    conn = db()
    conn.execute("INSERT INTO data (com,brand,mrp) VALUES (?,?,?)",
                 (request.form["com"], request.form["brand"], request.form["mrp"]))
    conn.commit()
    return "Added! <a href='/'>Back</a>"

# view data
@app.route("/view")
def view():
    conn = db()
    data = conn.execute("SELECT * FROM data").fetchall()
    return str(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
