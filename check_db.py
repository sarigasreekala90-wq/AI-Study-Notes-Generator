"""
Database Inspection Utility
This script prints the contents of all database tables for debugging purposes.
Run this from the project root to inspect the SQLite database.

Usage:
    python check_db.py

The script will display:
    - All registered users (without passwords)
    - All notes in the notes table
    - All generated notes with their topics and creation timestamps
"""

import sqlite3

def check_database():
    """Connect to database and print all table contents"""
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # Display Users
        print("=" * 60)
        print("USERS TABLE")
        print("=" * 60)
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        if users:
            print(f"{'ID':<5} {'Username':<20} {'Email':<30}")
            print("-" * 60)
            for user in users:
                print(f"{user[0]:<5} {user[1]:<20} {user[2]:<30}")
        else:
            print("No users found.")

        # Display Notes
        print("\n" + "=" * 60)
        print("NOTES TABLE")
        print("=" * 60)
        cur.execute("SELECT id, user, content FROM notes")
        notes = cur.fetchall()
        if notes:
            print(f"{'ID':<5} {'User':<20} {'Content':<35}")
            print("-" * 60)
            for note in notes:
                content_preview = note[2][:30] + "..." if len(note[2]) > 30 else note[2]
                print(f"{note[0]:<5} {note[1]:<20} {content_preview:<35}")
        else:
            print("No notes found.")

        # Display Generated Notes
        print("\n" + "=" * 60)
        print("GENERATED NOTES TABLE")
        print("=" * 60)
        cur.execute(
            "SELECT id, user, topic, created_at FROM generated_notes ORDER BY created_at DESC"
        )
        gen_notes = cur.fetchall()
        if gen_notes:
            print(f"{'ID':<5} {'User':<20} {'Topic':<30} {'Created At':<20}")
            print("-" * 60)
            for note in gen_notes:
                created = note[3] if note[3] else "N/A"
                print(f"{note[0]:<5} {note[1]:<20} {note[2]:<30} {created:<20}")
        else:
            print("No generated notes found.")

        conn.close()
        print("\n✓ Database inspection complete.")
        
    except sqlite3.DatabaseError as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database()
