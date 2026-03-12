from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# 自动生成未来7天日期
days = []
for i in range(7):
    day = datetime.now() + timedelta(days=i)
    days.append(day.strftime("%m-%d"))

# 每天时间段
times = ["10:00", "11:00", "12:00", "13:00"]

# 预约记录
booking = {}

@app.route("/")
def home():
    return render_template("index.html", days=days)

@app.route("/day/<day>")
def day_page(day):

    return render_template(
        "times.html",
        day=day,
        times=times,
        booking=booking
    )

@app.route("/book", methods=["POST"])
def book():

    name = request.form["name"]
    day = request.form["day"]
    time = request.form["time"]

    key = f"{day}_{time}"

    if key in booking:
        return "该时间已被预约 <br><a href=' '>返回首页</a >"

    booking[key] = name

    return "预约成功 <br><a href='/'>返回首页</a >"

@app.route("/admin")
def admin():
    return render_template("admin.html", booking=booking)

if __name__ == "__main__":
    app.run()
