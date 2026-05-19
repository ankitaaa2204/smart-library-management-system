from tkinter import END, messagebox
import sqlite3


# ---------------- VIEW BOOKS ----------------
def view_books(connect_db, tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


# ---------------- SEARCH BOOK ----------------
def search_book(connect_db, tree, search_entry):
    for row in tree.get_children():
        tree.delete(row)

    keyword = search_entry.get()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM books
    WHERE LOWER(title) LIKE LOWER(?)
    OR LOWER(author) LIKE LOWER(?)
    OR LOWER(category) LIKE LOWER(?)
    OR LOWER(book_id) LIKE LOWER(?)
    """, (
        '%' + keyword + '%',
        '%' + keyword + '%',
        '%' + keyword + '%',
        '%' + keyword + '%'
    ))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


# ---------------- ADD BOOK ----------------
def add_book(
    connect_db,
    entry_id,
    entry_title,
    entry_author,
    entry_category,
    entry_quantity,
    clear_fields_function,
    view_books_function,
    update_stats_function
):
    if entry_id.get() == "" or entry_title.get() == "" or entry_quantity.get() == "":
        messagebox.showerror("Error", "Fill all required fields")
        return

    try:
        new_qty = int(entry_quantity.get())
    except:
        messagebox.showerror("Error", "Quantity must be number")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(quantity) FROM books")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    if total + new_qty > 3000:
        messagebox.showerror("Limit Reached", "Maximum capacity is 3000 books")
        conn.close()
        return

    try:
        cursor.execute(
            "INSERT INTO books VALUES(?,?,?,?,?)",
            (
                entry_id.get(),
                entry_title.get(),
                entry_author.get(),
                entry_category.get(),
                new_qty
            )
        )

        conn.commit()
        messagebox.showinfo("Success", "Book Added Successfully")

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Book ID already exists")

    conn.close()

    clear_fields_function()
    view_books_function()
    update_stats_function()


# ---------------- DELETE BOOK ----------------
def delete_book(
    connect_db,
    tree,
    clear_fields_function,
    view_books_function,
    update_stats_function
):
    selected = tree.focus()

    if selected == "":
        messagebox.showerror("Error", "Select a row first")
        return

    values = tree.item(selected, "values")
    book_id = values[0]

    conn = connect_db()
    cursor = conn.cursor()

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Delete selected book?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM books WHERE book_id=?",
            (book_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Book Deleted")

        clear_fields_function()
        view_books_function()
        update_stats_function()

    else:
        conn.close()


# ---------------- UPDATE BOOK ----------------
def update_book(
    connect_db,
    entry_id,
    entry_title,
    entry_author,
    entry_category,
    entry_quantity,
    clear_fields_function,
    view_books_function,
    update_stats_function
):
    if entry_id.get() == "":
        messagebox.showerror("Error", "Select book first")
        return

    if entry_title.get() == "" or entry_quantity.get() == "":
        messagebox.showerror("Error", "Fields cannot be empty")
        return

    try:
        new_qty = int(entry_quantity.get())
    except:
        messagebox.showerror("Error", "Quantity must be number")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(quantity) FROM books")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    cursor.execute(
        "SELECT quantity FROM books WHERE book_id=?",
        (entry_id.get(),)
    )

    old_qty = cursor.fetchone()[0]

    if total - old_qty + new_qty > 3000:
        messagebox.showerror(
            "Limit Exceeded",
            "Cannot exceed 3000 total books"
        )

        conn.close()
        return

    cursor.execute("""
    UPDATE books
    SET title=?, author=?, category=?, quantity=?
    WHERE book_id=?
    """, (
        entry_title.get(),
        entry_author.get(),
        entry_category.get(),
        new_qty,
        entry_id.get()
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Updated",
        "Book Updated Successfully"
    )

    clear_fields_function()
    view_books_function()
    update_stats_function()