from tkinter import END, messagebox


# ---------------- ISSUE BOOK ----------------
def issue_book(
    connect_db,
    entry_id,
    student_id_entry,
    view_books_function,
    update_stats_function
):
    book_id = entry_id.get()
    student_id = student_id_entry.get()

    if book_id == "" or student_id == "":
        messagebox.showerror(
            "Error",
            "Select book and enter student ID"
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id=?",
        (student_id,)
    )

    if cursor.fetchone() is None:
        messagebox.showerror(
            "Error",
            "Student not registered"
        )

        conn.close()
        return

    # Prevent duplicate issue
    cursor.execute("""
    SELECT * FROM issued_books
    WHERE student_id=? AND book_id=?
    """, (student_id, book_id))

    if cursor.fetchone():
        messagebox.showerror(
            "Error",
            "Book already issued to this student"
        )

        conn.close()
        return

    cursor.execute(
        "SELECT quantity, title FROM books WHERE book_id=?",
        (book_id,)
    )

    data = cursor.fetchone()

    if data is None:
        messagebox.showerror(
            "Error",
            "Book not found"
        )

        conn.close()
        return

    qty, title = data

    if qty <= 0:
        messagebox.showerror(
            "Error",
            "Book out of stock"
        )

        conn.close()
        return

    cursor.execute(
        "UPDATE books SET quantity = quantity - 1 WHERE book_id=?",
        (book_id,)
    )

    cursor.execute("""
    INSERT INTO issued_books(student_id, book_id, issue_date)
    VALUES (?, ?, DATE('now'))
    """, (student_id, book_id))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        f"{title} issued successfully"
    )

    student_id_entry.delete(0, END)

    view_books_function()
    update_stats_function()


# ---------------- RETURN BOOK ----------------
def return_book(
    connect_db,
    entry_id,
    student_id_entry,
    view_books_function,
    update_stats_function
):
    book_id = entry_id.get()
    student_id = student_id_entry.get()

    if book_id == "" or student_id == "":
        messagebox.showerror(
            "Error",
            "Select book and enter student ID"
        )

        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM issued_books
    WHERE book_id=? AND student_id=?
    AND return_date IS NULL
    """, (book_id, student_id))

    data = cursor.fetchone()

    if data is None:
        messagebox.showerror(
            "Error",
            "This book was not issued to this student"
        )

        conn.close()
        return

    cursor.execute("""
    UPDATE issued_books
    SET return_date = DATE('now')
    WHERE rowid = (
        SELECT rowid FROM issued_books
        WHERE student_id=? AND book_id=?
        AND return_date IS NULL
        LIMIT 1
    )
    """, (student_id, book_id))

    cursor.execute("""
    UPDATE books
    SET quantity = quantity + 1
    WHERE book_id=?
    """, (book_id,))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Book Returned"
    )

    view_books_function()
    update_stats_function()


# ---------------- CALCULATE FINE ----------------
def calculate_fine(connect_db):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT issue_date, return_date
    FROM issued_books
    WHERE return_date IS NOT NULL
    """)

    records = cursor.fetchall()

    total_fine = 0

    for issue, ret in records:
        cursor.execute(
            "SELECT julianday(?) - julianday(?)",
            (ret, issue)
        )

        days = int(cursor.fetchone()[0])

        if days > 7:
            fine = (days - 7) * 2
            total_fine += fine

    conn.close()

    messagebox.showinfo(
        "Fine",
        f"Total Fine Collected: ₹{total_fine}"
    )