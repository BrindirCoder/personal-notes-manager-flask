# 📝 Personal Notes Manager (Flask)

A simple and secure **personal notes web application** built with **Flask**. Users can register, log in, and manage their private notes (create, edit, delete) through a clean web interface. The project is beginner‑friendly and structured to help you learn how real Flask applications are organized.

---

## 🚀 Features

* 🔐 User authentication (login & logout)
* 📝 Create, read, update, and delete personal notes
* ⚠️ Flash messages for user feedback
* 🎨 Simple UI with HTML & CSS
* 🧱 Modular Flask structure (routes, templates, static files)
* 🗄️ Database support using SQLAlchemy

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, Jinja2
* **Database:** SQLite (via SQLAlchemy)
* **Auth:** Flask‑Login

---

## 📂 Project Structure

```
Personal_notes_manager/
│
├── app.py                # App entry point
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── instance/
│   └── database.db       # SQLite database (auto‑created)
│
├── routes/
│   ├── auth.py           # Authentication routes
│   └── data.py           # Notes CRUD routes
│
├── templates/
│   ├── base.html         # Base layout
│   ├── index.html        # Notes page
│   └── login.html        # Login page
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── flash.css
│   └── js/
│
└── venv/            
```

---

## ✅ Requirements

Before running the project, make sure you have:

* Python **3.9+** installed
* pip (Python package manager)

---

## ⚙️ Installation & Setup (Step by Step)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/BrindirCoder/personal-notes-manager-flask.git
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

```bash
python app.py
```

### 5️⃣ Open in browser

Go to:

```
http://127.0.0.1:5000
```

---

## 🧪 How to Use

1. Register or log in
2. Add a new note
3. Edit or delete existing notes
4. Log out securely

All notes are private to the logged‑in user.

---

## 🔒 Security Notes

* Passwords are hashed (not stored in plain text)
* Routes are protected using `@login_required`


---


## 📜 License

This project is open‑source and free to use for learning and personal projects.

---

## 🙌 Author

Built by **alo**

If you find this useful, don’t forget to ⭐ the repository!
