from flask import Flask, render_template, request

app = Flask(__name__)

# 预约数据
days = ["周一", "周二", "周三"]
times = ["10:00", "11:00", "12:00"]

booking = {}

@app.route("/")
def home():
    return render_template(
        "index.html",
        days=days,
        times=times,
        booking=booking
    )

@app.route("/book", methods=["POST"])
def book():

    day = request.form["day"]
    time = request.form["time"]

    key = f"{day}_{time}"

    if key in booking:
        return "该时间已被预约"

    booking[key] = "已预约"

    return "预约成功 <br><a href=' '>返回</a >"


if __name__ == "__main__":
    app.run()
