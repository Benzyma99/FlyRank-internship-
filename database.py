import sqlite3

connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL
)
""")
connection.commit()
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]
if count == 0:
    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        [
            ("Learn FastAPI", 0),
            ("Finish Assignment", 0),
            ("Practice SQLite", 0)
        ]
    )

    connection.commit()