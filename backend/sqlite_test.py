# python -c "import sqlite3; c=sqlite3.connect('backend/test.db'); print(c.execute('SELECT * FROM test_items').fetchall())"
# Run the above command in root terminal.

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "test.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cur.execute("INSERT INTO test_items (name) VALUES (?)", ("it works",))
    conn.commit()
    cur.execute("SELECT id, name FROM test_items ORDER BY id DESC LIMIT 5")
    print("Latest rows:", cur.fetchall())
    conn.close()
    print("DB file at:", DB_PATH)


if __name__ == "__main__":
    main()
