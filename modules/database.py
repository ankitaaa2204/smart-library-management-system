import sqlite3


# ---------------- CONNECT DATABASE ----------------
def connect_db():
    return sqlite3.connect("library.db")


# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # BOOKS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        book_id TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        category TEXT,
        quantity INTEGER
    )
    """)

    # STUDENTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY,
        name TEXT,
        course TEXT
    )
    """)

    # ISSUED BOOKS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued_books(
        student_id TEXT,
        book_id TEXT,
        issue_date TEXT,
        return_date TEXT
    )
    """)

    conn.commit()
    conn.close()