from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

ADMIN_PASSWORD = "123456"

DB="booking.db"


# ==============================
# 初始化数据库
# ==============================

def init_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    time TEXT,
    name TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ==============================
# 预约页面
# ==============================

@app.route("/")
def index():

    days=["周一","周二","周三","周四","周五"]

    times=["10:00","11:00","14:00","15:00"]

    conn=sqlite3.connect(DB)
    cursor=conn.cursor()

    cursor.execute("SELECT day,time,name FROM bookings")

    rows=cursor.fetchall()

    conn.close()

    booking_dict={}

    for r in rows:

        booking_dict[f"{r[0]}_{r[1]}"]=r[2]

    return render_template(
        "index.html",
        days=days,
        times=times,
        booking_dict=booking_dict
    )


# ==============================
# 提交预约
# ==============================

@app.route("/book",methods=["POST"])
def book():

    name=request.form["name"]
    day=request.form["day"]
    time=request.form["time"]

    conn=sqlite3.connect(DB)
    cursor=conn.cursor()

    cursor.execute(
    "SELECT * FROM bookings WHERE day=? AND time=?",
    (day,time)
    )

    exist=cursor.fetchone()

    if exist:

        conn.close()

        return "该时间已被预约"

    cursor.execute(
    "INSERT INTO bookings(day,time,name) VALUES(?,?,?)",
    (day,time,name)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# ==============================
# 后台管理
# ==============================

@app.route("/admin")
def admin():

    pwd=request.args.get("pwd")

    if pwd!=ADMIN_PASSWORD:

        return "密码错误"

    conn=sqlite3.connect(DB)
    cursor=conn.cursor()

    cursor.execute("SELECT id,day,time,name FROM bookings")

    rows=cursor.fetchall()

    conn.close()

    return render_template("admin.html",rows=rows,pwd=pwd)


# ==============================
# 删除预约
# ==============================

@app.route("/delete/<int:id>")
def delete(id):

    pwd=request.args.get("pwd")

    if pwd!=ADMIN_PASSWORD:

        return "无权限"

    conn=sqlite3.connect(DB)
    cursor=conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect(f"/admin?pwd={pwd}")


# ==============================
# 导出Excel
# ==============================

@app.route("/export")
def export():

    pwd=request.args.get("pwd")

    if pwd!=ADMIN_PASSWORD:

        return "无权限"

    conn=sqlite3.connect(DB)

    df=pd.read_sql_query("SELECT day,time,name FROM bookings",conn)

    conn.close()

    file="booking.xlsx"

    df.to_excel(file,index=False)

    return send_file(file,as_attachment=True)


# ==============================
# 统计图表
# ==============================

@app.route("/chart")
def chart():

    pwd=request.args.get("pwd")

    if pwd!=ADMIN_PASSWORD:

        return "无权限"

    conn=sqlite3.connect(DB)
    cursor=conn.cursor()

    cursor.execute("""
    SELECT day,count(*)
    FROM bookings
    GROUP BY day
    """)

    rows=cursor.fetchall()

    conn.close()

    return rows


# ==============================
# 启动
# ==============================

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)
