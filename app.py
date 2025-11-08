import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_API = os.getenv("BACKEND_API_URL", "http://localhost:5000/api")
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "devsecret")
SESSION_TYPE = "filesystem"

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_TYPE"] = SESSION_TYPE
app.config["TEMPLATES_AUTO_RELOAD"] = False
Session(app)

# Helpers
def api_post(path, json=None, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(f"{BACKEND_API}{path}", json=json, headers=headers, timeout=10)

def api_get(path, params=None, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(f"{BACKEND_API}{path}", params=params, headers=headers, timeout=10)

def api_delete(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.delete(f"{BACKEND_API}{path}", headers=headers, timeout=10)

# Auth helpers
def is_authenticated():
    return "token" in session

def current_user():
    return session.get("user")

def require_auth():
    if not is_authenticated():
        return redirect(url_for("login"))

# Public
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            resp = api_post("/auth/login", json={"email": email, "password": password})
            resp.raise_for_status()
            data = resp.json()
            session["token"] = data["token"]
            session["user"] = data["user"]
            # role-based redirect
            if data["user"].get("role") == "admin":
                return redirect(url_for("admin_panel"))
            return redirect(url_for("dashboard"))
        except requests.HTTPError as e:
            msg = e.response.json().get("message") if e.response is not None else str(e)
            flash(msg or "Login failed", "danger")
    # GET
    if is_authenticated():
        # if already logged in, redirect by role
        u = current_user()
        if u and u.get("role") == "admin":
            return redirect(url_for("admin_panel"))
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            resp = api_post("/auth/register", json={"name": name, "email": email, "password": password})
            resp.raise_for_status()
            data = resp.json()
            session["token"] = data["token"]
            session["user"] = data["user"]
            return redirect(url_for("dashboard"))
        except requests.HTTPError as e:
            msg = e.response.json().get("message") if e.response is not None else str(e)
            flash(msg or "Registration failed", "danger")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Protected pages
@app.route("/")
def dashboard():
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    reminders = []
    try:
        res = api_get("/reminders", token=token)
        res.raise_for_status()
        reminders = res.json()
    except Exception:
        reminders = []
    return render_template("dashboard.html", user=current_user(), reminders=reminders)

@app.route("/exams", methods=["GET", "POST"])
def exams():
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    if request.method == "POST":
        # create exam
        title = request.form.get("title")
        subject = request.form.get("subject")
        date = request.form.get("date")
        priority = int(request.form.get("priority") or 0)
        try:
            res = api_post("/exams", json={"title": title, "subject": subject, "date": date, "priority": priority}, token=token)
            res.raise_for_status()
            flash("Exam created.", "success")
        except Exception as e:
            flash("Failed to create exam.", "danger")
        return redirect(url_for("exams"))
    # GET: list exams
    sortBy = request.args.get("sortBy", "date")
    exams = []
    try:
        res = api_get("/exams", params={"sortBy": sortBy}, token=token)
        res.raise_for_status()
        exams = res.json()
    except Exception:
        exams = []
    return render_template("exams.html", exams=exams)

@app.route("/exams/<id>", methods=["POST"])
def delete_exam(id):
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    try:
        res = api_delete(f"/exams/{id}", token=token)
        if res.status_code == 200:
            flash("Deleted exam.", "success")
        else:
            flash("Failed to delete.", "danger")
    except Exception:
        flash("Failed to delete.", "danger")
    return redirect(url_for("exams"))

@app.route("/notes", methods=["GET", "POST"])
def notes():
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        parentNote = request.form.get("parentNote") or None
        try:
            res = api_post("/notes", json={"title": title, "content": content, "parentNote": parentNote}, token=token)
            res.raise_for_status()
            flash("Note added.", "success")
        except Exception:
            flash("Failed to add note.", "danger")
        return redirect(url_for("notes"))
    # GET
    notes_tree = []
    try:
        res = api_get("/notes", token=token)
        res.raise_for_status()
        notes_tree = res.json()
    except Exception:
        notes_tree = []
    return render_template("notes.html", notes=notes_tree)

@app.route("/notes/<id>", methods=["POST"])
def delete_note(id):
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    try:
        res = api_delete(f"/notes/{id}", token=token)
        if res.status_code == 200:
            flash("Deleted note.", "success")
        else:
            flash("Failed to delete.", "danger")
    except Exception:
        flash("Failed to delete.", "danger")
    return redirect(url_for("notes"))

@app.route("/reminders", methods=["GET", "POST"])
def reminders():
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    # fetch exams for dropdown
    exams = []
    try:
        res = api_get("/exams", token=token)
        res.raise_for_status()
        exams = res.json()
    except Exception:
        exams = []
    if request.method == "POST":
        message = request.form.get("message")
        remindAt = request.form.get("remindAt")
        examId = request.form.get("examId")
        if not (message and remindAt and examId):
            flash("All fields required.", "danger")
            return redirect(url_for("reminders"))
        try:
            res = api_post("/reminders", json={"message": message, "remindAt": remindAt, "examId": examId}, token=token)
            res.raise_for_status()
            flash("Reminder created.", "success")
        except Exception:
            flash("Failed to create reminder.", "danger")
        return redirect(url_for("reminders"))
    # GET: list reminders
    reminders = []
    try:
        res = api_get("/reminders", token=token)
        res.raise_for_status()
        reminders = res.json()
    except Exception:
        reminders = []
    return render_template("reminders.html", reminders=reminders, exams=exams)

@app.route("/reminders/<id>", methods=["POST"])
def delete_reminder(id):
    if not is_authenticated():
        return redirect(url_for("login"))
    token = session["token"]
    try:
        res = api_delete(f"/reminders/{id}", token=token)
        if res.status_code == 200:
            flash("Deleted reminder.", "success")
        else:
            flash("Failed to delete.", "danger")
    except Exception:
        flash("Failed to delete.", "danger")
    return redirect(url_for("reminders"))

@app.route("/admin")
def admin_panel():
    if not is_authenticated():
        return redirect(url_for("login"))
    user = current_user()
    if user.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))
    token = session["token"]
    users = []
    exams = []
    try:
        ures = api_get("/admin/users", token=token); ures.raise_for_status(); users = ures.json()
        eres = api_get("/admin/exams", token=token); eres.raise_for_status(); exams = eres.json()
    except Exception:
        users = []; exams = []
    return render_template("admin.html", users=users, exams=exams)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=3000)
