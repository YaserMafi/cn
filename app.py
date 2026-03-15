from flask import Flask, request, render_template_string
import psutil
import platform
import datetime

app = Flask(__name__)

# --------------------------
# صفحه اصلی
# --------------------------

home_page = """
<h2>Control Panel</h2>

<a href="/panel/status/admin">System Status</a><br><br>
<a href="/panel/control/admin">System Control</a>
"""

@app.route("/")
def home():
    return home_page


# --------------------------
# صفحه وضعیت سیستم
# --------------------------

panel_status_page = """
<h2>System Status - {{user}}</h2>

Memory: {{memory_used}} / {{memory_total}} MB<br>
CPU Usage: {{cpu_percent}} %<br>
Battery: {{battery_percent}} %<br>
Time: {{time}}<br><br>

<a href="/">Back</a>
"""

@app.route("/panel/status/<user>")
def panel_status(user):

    memory = psutil.virtual_memory()
    battery = psutil.sensors_battery()

    memory_used = round(memory.used/1024/1024)
    memory_total = round(memory.total/1024/1024)

    cpu_percent = psutil.cpu_percent()

    battery_percent = battery.percent if battery else "Unknown"

    time = datetime.datetime.now()

    return render_template_string(
        panel_status_page,
        user=user,
        memory_used=memory_used,
        memory_total=memory_total,
        cpu_percent=cpu_percent,
        battery_percent=battery_percent,
        time=time
    )


# --------------------------
# صفحه کنترل
# --------------------------

panel_control_page = """

<h2>Control Panel - {{user}}</h2>

<form method="post">

<button name="action" value="show_info">Show Info</button>

</form>

<br>

{{info}}

<br><br>

<a href="/">Back</a>

"""

@app.route("/panel/control/<user>", methods=["GET","POST"])
def panel_control(user):

    info = ""

    if request.method=="POST":

        action = request.form.get("action")

        if action=="show_info":

            memory = psutil.virtual_memory()
            battery = psutil.sensors_battery()
            cpu_percent = psutil.cpu_percent()

            info = f"""
            Memory: {round(memory.used/1024/1024)} / {round(memory.total/1024/1024)} MB<br>
            CPU: {cpu_percent}%<br>
            Battery: {battery.percent if battery else 'Unknown'}%
            """

    return render_template_string(panel_control_page, user=user, info=info)


# --------------------------
# اجرای سرور
# --------------------------

if __name__ == "main":
    app.run(host="0.0.0.0", port=10000)