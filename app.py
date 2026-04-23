from flask import Flask, request, redirect
import sqlite3, os

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def db():
    return sqlite3.connect("data.db")

# create table
conn = db()
conn.execute("""CREATE TABLE IF NOT EXISTS data (
id INTEGER PRIMARY KEY,
com TEXT,
brand TEXT,
mrp TEXT,
pre TEXT,
ptr TEXT,
length TEXT,
sticks TEXT,
market TEXT,
image TEXT
)""")
conn.commit()

@app.route("/")
def home():
    return """
    <h2>Admin Panel</h2>
    <form method='POST' action='/add' enctype='multipart/form-data'>
    COM:<input name='com'><br>
    BRAND:<input name='brand'><br>
    MRP:<input name='mrp'><br>
    PRE STICK PRICE:<input name='pre'><br>
    PTR:<input name='ptr'><br>
    CIG LENGTH:<input name='length'><br>
    NUMBER OF STICKS:<input name='sticks'><br>
    MARKET:<input name='market'><br>
    IMAGE:<input type='file' name='image'><br>
    <button>Add</button>
    </form>
    <br><a href='/view'>View Data</a>
    """

@app.route("/add", methods=["POST"])
def add():
    file = request.files["image"]
    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    conn = db()
    conn.execute("""INSERT INTO data 
    (com,brand,mrp,pre,ptr,length,sticks,market,image)
    VALUES (?,?,?,?,?,?,?,?,?)""",
    (
        request.form["com"],
        request.form["brand"],
        request.form["mrp"],
        request.form["pre"],
        request.form["ptr"],
        request.form["length"],
        request.form["sticks"],
        request.form["market"],
        filename
    ))
    conn.commit()

    return "Data Added ✅ <br><a href='/'>Back</a>"

@app.route("/view")
def view():
    conn = db()
    data = conn.execute("SELECT * FROM data").fetchall()

    html = "<h2>Data List</h2>"
    for d in data:
        html += f"""
        <hr>
        COM: {d[1]}<br>
        BRAND: {d[2]}<br>
        MRP: {d[3]}<br>
        PRE: {d[4]}<br>
        PTR: {d[5]}<br>
        LENGTH: {d[6]}<br>
        STICKS: {d[7]}<br>
        MARKET: {d[8]}<br>
        IMAGE: {d[9]}<br>
        """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
