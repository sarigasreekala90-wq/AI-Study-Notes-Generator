from flask import Flask, render_template, request, redirect, session, jsonify
import ollama
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from datetime import datetime

app = Flask(__name__)
# Use environment variable for secret key with secure fallback
app.secret_key = os.environ.get("SECRET_KEY", "your-secure-secret-key-change-in-production")


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

    prompt = f"""
Create beginner-friendly study notes on {topic}.

Give the notes in the following format:

Definition:
Key Points:
Advantages:
Applications:
Example:
Summary:

Use simple English suitable for engineering students.
"""

    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    return {
        "topic": topic.title(),
        "definition": text,
        "key_points": "",
        "advantages": "",
        "applications": "",
        "example": "",
        "summary": text
    }

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("home.html")

# ---------- VALIDATION FUNCTIONS ----------
def validate_username(username):
    """Validate username: 3-20 characters, alphanumeric and underscores only"""
    if not username or len(username) < 3 or len(username) > 20:
        return "Username must be 3-20 characters long."
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return "Username can only contain letters, numbers, and underscores."
    return None

def validate_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return "Please enter a valid email address."
    return None

def validate_password(password):
    """Validate password: at least 6 characters"""
    if not password or len(password) < 6:
        return "Password must be at least 6 characters long."
    return None

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    username = ""
    email = ""
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Validate inputs
        error = validate_username(username) or validate_email(email) or validate_password(password)
        
        if not error:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            try:
                # Check if email already exists
                cur.execute("SELECT id FROM users WHERE email=?", (email,))
                if cur.fetchone():
                    error = "This email is already registered. Please login or use a different email."
                else:
                    # Hash password and insert user
                    hashed = generate_password_hash(password)
                    cur.execute(
                        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                        (username, email, hashed)
                    )
                    conn.commit()
                    conn.close()
                    return redirect("/login?success=Account created successfully! Please login.")
            except sqlite3.IntegrityError as e:
                error = "An error occurred during registration. Please try again."
            finally:
                conn.close()

    return render_template("register.html", error=error, username=username, email=email)

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    success = request.args.get("success")
    email = ""
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            error = "Please enter both email and password."
        else:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            try:
                cur.execute(
                    "SELECT id, username, password FROM users WHERE email=?",
                    (email,)
                )

                user = cur.fetchone()
                
                if not user:
                    error = "No account found with this email. Please register first."
                elif not check_password_hash(user[2], password):
                    error = "Incorrect password. Please try again."
                else:
                    # Login successful
                    session["user"] = user[1]  # Store username
                    conn.close()
                    return redirect("/dashboard")
            except Exception as e:
                error = "An error occurred during login. Please try again."
            finally:
                conn.close()

    return render_template("login.html", error=error, success=success, email=email)

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
        
        # Validate topic - prevent empty topics
        if not topic_value or len(topic_value) > 50:
            topic_value = ""
        else:
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

    # Fetch the most recent note if not just generated
    if generated_note is None:
        cur.execute(
            "SELECT id, topic, definition, key_points, advantages, applications, example, summary, created_at "
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
                "created_at": row[8],
            }

    # Fetch recent topics (last 5)
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


# ---------- DELETE GENERATED NOTE (API ENDPOINT) ----------
@app.route("/api/delete_note", methods=["POST"])
def delete_note_api():
    if "user" not in session:
        return jsonify({"success": False, "error": "Not authenticated"}), 403

    try:
        data = request.get_json() or {}
        note_id = data.get("id")
        
        if not note_id:
            return jsonify({"success": False, "error": "Invalid note ID"}), 400

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # Verify the note belongs to the current user
        cur.execute("SELECT user FROM generated_notes WHERE id=?", (note_id,))
        note = cur.fetchone()
        
        if not note or note[0] != session["user"]:
            conn.close()
            return jsonify({"success": False, "error": "Unauthorized"}), 403
        
        # Delete the note
        cur.execute("DELETE FROM generated_notes WHERE id=? AND user=?", (note_id, session["user"]))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "message": "Note deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ---------- SEARCH GENERATED NOTES ----------
@app.route("/api/search_notes")
def search_notes():
    if "user" not in session:
        return jsonify({"notes": []}), 403
    
    try:
        search_query = request.args.get("q", "").strip().lower()
        
        if not search_query or len(search_query) < 2:
            return jsonify({"notes": []})
        
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        cur.execute(
            "SELECT id, topic, created_at FROM generated_notes WHERE user=? AND LOWER(topic) LIKE ? ORDER BY created_at DESC LIMIT 10",
            (session["user"], f"%{search_query}%")
        )
        
        rows = cur.fetchall()
        notes = [{"id": row[0], "topic": row[1], "created_at": row[2]} for row in rows]
        conn.close()
        
        return jsonify({"notes": notes})
    except Exception as e:
        return jsonify({"notes": [], "error": str(e)})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)