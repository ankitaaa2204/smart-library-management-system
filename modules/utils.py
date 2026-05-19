from tkinter import END


# ---------------- UPDATE STATS ----------------
def update_stats(connect_db, title_count_label, qty_count_label):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_titles = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(quantity) FROM books")
    total_qty = cursor.fetchone()[0]

    if total_qty is None:
        total_qty = 0

    title_count_label.config(text=f"Total Titles: {total_titles}")
    qty_count_label.config(text=f"Total Books: {total_qty}/300")

    conn.close()


# ---------------- CLEAR FIELDS ----------------
def clear_fields(
    entry_id,
    entry_title,
    entry_author,
    entry_category,
    entry_quantity,
    student_entry,
    student_id_entry,
    student_name_entry,
    student_course_entry
):
    entry_id.delete(0, END)
    entry_title.delete(0, END)
    entry_author.delete(0, END)
    entry_category.delete(0, END)
    entry_quantity.delete(0, END)
    student_entry.delete(0, END)
    student_id_entry.delete(0, END)
    student_name_entry.delete(0, END)
    student_course_entry.delete(0, END)


# ---------------- SELECT ROW ----------------
def select_row(
    event,
    tree,
    clear_fields_function,
    entry_id,
    entry_title,
    entry_author,
    entry_category,
    entry_quantity
):
    selected = tree.focus()
    values = tree.item(selected, "values")

    if values:
        clear_fields_function()

        entry_id.insert(0, values[0])
        entry_title.insert(0, values[1])
        entry_author.insert(0, values[2])
        entry_category.insert(0, values[3])
        entry_quantity.insert(0, values[4])