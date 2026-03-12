from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# 数据库连接
conn = sqlite3.connect("booking.db", check_same_thread=False)
cursor = conn.cursor()

# 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
day TEXT,
time TEXT,
name TEXT
)
""")

conn.commit()

days = ["周一","周二","周三"]
times = ["10:00","11:00","12:00"]

@app.route("/")
def home():

    cursor.execute("SELECT day,time,name FROM bookings")
    rows = cursor.fetchall()

    booking = {}

    for r in rows:
        key = r[0]+"_"+r[1]
        booking[key] = r[2]

    return render_template(
        "index.html",
        days=days,
        times=times,
        booking=booking
    )

@app.route("/book", methods=["POST"])
def book():

    name = request.form["name"]
    day = request.form["day"]
    time = request.form["time"]

    cursor.execute(
        "SELECT * FROM bookings WHERE day=? AND time=?",
        (day,time)
    )

    result = cursor.fetchone()

    if result:
        return "该时间已被预约 <br><a href=' '>返回</a >"

    cursor.execute(
        "INSERT INTO bookings (day,time,name) VALUES (?,?,?)",
        (day,time,name)
    )

    conn.commit()

    return "预约成功 <br><a href='/'>返回</a >"

@app.route("/admin")
def admin():

    cursor.execute("SELECT day,time,name FROM bookings")

    rows = cursor.fetchall()

    return render_template(
        "admin.html",
        rows=rows
    )

# ⭐ Render 必须这样启动
if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
