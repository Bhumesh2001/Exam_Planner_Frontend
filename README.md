# 🎓 The Exam Planner & Reminder System — Frontend (Flask + HTML/CSS + JS)

A clean and modern **Flask-based frontend** for _The Exam Planner & Reminder System_, built to manage **Exams, Notes, and Reminders**.
It provides a secure login system, dashboard, and CRUD interfaces — all styled with a modern dark theme inspired by the original MERN version.

---

## 🚀 Features

- 🔐 Secure login and registration pages
- 🏠 Dashboard showing upcoming reminders
- 🎓 Exams management (add, sort, delete)
- 🗒️ Notes section with nested hierarchy
- ⏰ Reminder creation (linked to specific exams)
- 🧭 Role-based navigation (Admin / User)
- 🌓 Dark, modern, and responsive UI using Tailwind CSS

---

## 🧩 Tech Stack

- **Python Flask** — Frontend framework
- **Flask-Session** — User session management
- **HTML5 / Jinja2 Templates** — Dynamic rendering
- **Tailwind CSS** — Modern UI styling
- **JavaScript (Fetch API)** — API communication
- **Font Awesome / Lucide Icons** — Icons and visual polish

---

## 📁 Folder Structure

```
frontend/
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── exams.html
│   ├── notes.html
│   ├── reminders.html
│   └── admin.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── assets/
│       └── logo.png
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/exam-planner-frontend.git
cd exam-planner-frontend
```

---

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If missing, create a `requirements.txt` file:

```bash
Flask
Flask-Session
python-dotenv
requests
```

---

### 4. Configure environment variables

Create a `.env` file in your project root:

```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
BACKEND_API_URL=http://127.0.0.1:5000/api
SESSION_TYPE=filesystem
```

---

### 5. Run the Flask frontend

```bash
python app.py
```

Your frontend will be available at:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧠 Pages Overview

### 🔑 `/login`

User login page with email and password form.
Automatically redirects to `/dashboard` after successful login.

### 🧾 `/register`

Simple registration page for new users with password confirmation.

### 🏠 `/dashboard`

Displays:

- Upcoming reminders
- Navigation to Exams, Notes, and Admin (if applicable)

### 🎓 `/exams`

- Create, view, and delete exams
- Sort by title, date, or priority

### 🗒️ `/notes`

- Create notes (optional parent-child structure)
- Delete notes recursively

### ⏰ `/reminders`

- Add reminders linked to exams
- View and delete existing reminders

### 🧑‍💼 `/admin`

Admin-only page listing:

- All users
- All exams (with user references)

---

## 🎨 UI / Styling

The frontend uses **Tailwind CSS** for a modern, dark aesthetic.

Key colors:

- Background: `#0f172a` (Dark Navy)
- Primary: `#2563eb` (Blue)
- Accent: `#38bdf8` (Sky)
- Text: White and gray tones

Responsive grid and flex utilities ensure a clean layout across all devices.

---

## 🔄 API Communication

All frontend requests use the Python `requests` module or Fetch API, connecting to the backend Flask API:

Example:

```python
response = requests.get(f"{BACKEND_API_URL}/exams", cookies=session['cookies'])
```

Or via JavaScript (AJAX):

```js
fetch("/api/exams", {
  method: "GET",
  headers: { "Content-Type": "application/json" },
});
```

---

## 🧩 Authentication Flow

1. User registers → backend creates account
2. Login → session created via Flask-Session
3. Protected routes require valid session
4. Logout → session cleared and redirected to `/login`

---

## 🧠 Example `.env` (Full)

```bash
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=exam_planner_secret
BACKEND_API_URL=http://127.0.0.1:5000/api
SESSION_TYPE=filesystem
```

---

## 🌍 Deployment

You can deploy this Flask frontend to:

- **Render**
- **PythonAnywhere**
- **Heroku**
- **Vercel (via WSGI adapter)**

Make sure:

- Backend API is deployed and accessible
- Environment variables match your production setup

---

## 👨‍💻 Author

**Bhumesh Kewat**
Software Engineer | Full Stack Developer
📧 [bhumesh21@navgurukul.org](mailto:bhumesh21@navgurukul.org)

---

## 🪪 License

This project is open source and available under the **MIT License**.

---

**✨ Built with Flask, Tailwind CSS, and pure passion — The Exam Planner & Reminder System (Frontend).**
