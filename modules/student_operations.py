from tkinter import messagebox


# ---------------- ADD STUDENT ----------------
def add_student(
    connect_db,
    student_id_entry,
    student_name_entry,
    student_course_entry
):
    sid = student_id_entry.get()
    name = student_name_entry.get()
    course = student_course_entry.get()

    if sid == "" or name == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students VALUES(?,?,?)",
            (sid, name, course)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student Added"
        )

    except:
        messagebox.showerror(
            "Error",
            "Student already exists"
        )

    conn.close()