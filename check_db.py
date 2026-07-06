import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

print("Users:")
cur.execute("SELECT * FROM users")
print(cur.fetchall())

print("\nNotes:")
cur.execute("SELECT * FROM notes")
print(cur.fetchall())

print("\nGenerated Notes:")
cur.execute("SELECT * FROM generated_notes")
print(cur.fetchall())

conn.close()