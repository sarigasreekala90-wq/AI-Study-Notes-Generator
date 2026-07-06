from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- INIT DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

def init_notes_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_notes_table()

# ---------- GENERATED NOTES TABLE ----------
def init_generated_notes_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS generated_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        topic TEXT NOT NULL,
        definition TEXT NOT NULL,
        key_points TEXT NOT NULL,
        advantages TEXT NOT NULL,
        applications TEXT NOT NULL,
        example TEXT NOT NULL,
        summary TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_generated_notes_table()

def generate_study_notes(topic):
    topic_title = topic.strip().title()
    return {
        "topic": topic_title,
        "definition": f"{topic_title} describes the key principles and structure needed to understand the subject clearly.",
        "key_points": (
            f"1. Core concepts of {topic_title}.\n"
            f"2. Important terminology and use cases.\n"
            f"3. Practical steps to apply {topic_title} in study or projects."
        ),
        "advantages": (
            f"- Helps you build a reliable foundation in {topic_title}.\n"
            f"- Improves problem solving and decision making.\n"
            f"- Makes it easier to learn advanced topics later."
        ),
        "applications": (
            f"- Common scenarios where {topic_title} is useful.\n"
            f"- How {topic_title} connects with other study domains.\n"
            f"- Projects and real-world examples where {topic_title} applies."
        ),
        "example": (
            f"Imagine using {topic_title} to solve a practical task, then reviewing the steps and outcomes. "
            f"This example reinforces how the concepts work in context."
        ),
        "summary": (
            f"{topic_title} is a foundational concept worth mastering. "
            f"Use these notes to review definitions, key points, advantages, and applications quickly."
        )
    }

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("home.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        try:
            hashed = generate_password_hash(password)
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            conn.close()
            return "User already exists!"

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user"] = user[1]
            return redirect("/dashboard")
        else:
            return "Invalid login!"

    return render_template("login.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    generated_note = None
    topic_value = ""

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        topic_value = request.form.get("topic", "").strip()
        if topic_value:
            generated_note = generate_study_notes(topic_value)
            cur.execute(
                "INSERT INTO generated_notes (user, topic, definition, key_points, advantages, applications, example, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    session["user"],
                    generated_note["topic"],
                    generated_note["definition"],
                    generated_note["key_points"],
                    generated_note["advantages"],
                    generated_note["applications"],
                    generated_note["example"],
                    generated_note["summary"],
                ),
            )
            conn.commit()
            generated_id = cur.lastrowid
            generated_note["id"] = generated_id

    if generated_note is None:
        cur.execute(
            "SELECT id, topic, definition, key_points, advantages, applications, example, summary "
            "FROM generated_notes WHERE user=? ORDER BY created_at DESC LIMIT 1",
            (session["user"],),
        )
        row = cur.fetchone()
        if row:
            generated_note = {
                "id": row[0],
                "topic": row[1],
                "definition": row[2],
                "key_points": row[3],
                "advantages": row[4],
                "applications": row[5],
                "example": row[6],
                "summary": row[7],
            }

    cur.execute(
        "SELECT topic FROM generated_notes WHERE user=? ORDER BY created_at DESC LIMIT 5",
        (session["user"],),
    )
    recent_topics = [row[0] for row in cur.fetchall()]
    conn.close()

    return render_template(
        "dashboard.html",
        user=session["user"],
        generated_note=generated_note,
        recent_topics=recent_topics,
        topic_value=topic_value,
    )

# ---------- ADD NOTE ----------
@app.route("/add_note", methods=["POST"])
def add_note():
    if "user" not in session:
        return redirect("/login")

    content = request.form["content"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO notes (user, content) VALUES (?, ?)",
                (session["user"], content))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ---------- DELETE GENERATED NOTE ----------
@app.route("/delete_generated_note", methods=["POST"])
def delete_generated_note():
    if "user" not in session:
        return ("", 403)

    data = request.get_json()
    note_id = data.get("id") if data else None
    if not note_id:
        return ("", 400)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM generated_notes WHERE id=? AND user=?", (note_id, session["user"]))
    conn.commit()
    conn.close()

    return ("", 204)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)