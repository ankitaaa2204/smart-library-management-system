from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from modules.database import connect_db

# ===================ISSUED BOOKS WINDOW===================
def show_issued_books():

    issued_window = Toplevel()
    issued_window.title("Issued Books")
    issued_window.geometry("900x500")
    issued_window.config(bg="white")

    # ---------- TITLE ----------
    Label(
        issued_window,
        text="ISSUED BOOKS RECORD",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="darkblue"
    ).pack(pady=10)

    # ---------- FRAME ----------
    table_frame = Frame(issued_window)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ---------- SCROLLBARS ----------
    scroll_y = Scrollbar(table_frame, orient=VERTICAL)
    scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

    # ---------- TREEVIEW ----------
    issued_tree = ttk.Treeview(
        table_frame,
        columns=(
            "Student ID",
            "Book ID",
            "Issue Date",
            "Return Date",
            "Status"
        ),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=issued_tree.yview)
    scroll_x.config(command=issued_tree.xview)

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)

    issued_tree.pack(fill=BOTH, expand=True)

    # ---------- HEADINGS ----------
    issued_tree.heading("Student ID", text="Student ID")
    issued_tree.heading("Book ID", text="Book ID")
    issued_tree.heading("Issue Date", text="Issue Date")
    issued_tree.heading("Return Date", text="Return Date")
    issued_tree.heading("Status", text="Status")

    # ---------- COLUMN WIDTH ----------
    issued_tree.column("Student ID", width=150)
    issued_tree.column("Book ID", width=150)
    issued_tree.column("Issue Date", width=150)
    issued_tree.column("Return Date", width=150)
    issued_tree.column("Status", width=150)

    # ---------- DATABASE ----------
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            book_id,
            issue_date,
            return_date
        FROM issued_books
    """)

    rows = cursor.fetchall()

    # ---------- INSERT DATA ----------
    for row in rows:

        status = "Returned"

        if row[3] is None:
            status = "Not Returned"

        issued_tree.insert(
            "",
            END,
            values=(
                row[0],
                row[1],
                row[2],
                row[3],
                status
            )
        )

    conn.close()


# ===================STUDENT RECORD WINDOW===================
def show_students():

    student_window = Toplevel()
    student_window.title("Student Records")
    student_window.geometry("700x450")
    student_window.config(bg="white")

    # ---------- TITLE ----------
    Label(
        student_window,
        text="STUDENT RECORDS",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="darkblue"
    ).pack(pady=10)

    # ---------- FRAME ----------
    table_frame = Frame(student_window)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ---------- SCROLLBARS ----------
    scroll_y = Scrollbar(table_frame, orient=VERTICAL)
    scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

    # ---------- TREEVIEW ----------
    student_tree = ttk.Treeview(
        table_frame,
        columns=(
            "Student ID",
            "Name",
            "Course"
        ),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=student_tree.yview)
    scroll_x.config(command=student_tree.xview)

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)

    student_tree.pack(fill=BOTH, expand=True)

    # ---------- HEADINGS ----------
    student_tree.heading("Student ID", text="Student ID")
    student_tree.heading("Name", text="Student Name")
    student_tree.heading("Course", text="Course")

    # ---------- COLUMN WIDTH ----------
    student_tree.column("Student ID", width=150)
    student_tree.column("Name", width=250)
    student_tree.column("Course", width=200)

    # ---------- DATABASE ----------
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students
    """)

    rows = cursor.fetchall()

    # ---------- INSERT DATA ----------
    for row in rows:

        student_tree.insert(
            "",
            END,
            values=row
        )

    conn.close()


    
# ===================STUDENT FINE WINDOW===================
def show_student_fines():

    fine_window = Toplevel()
    fine_window.title("Student Fine Records")
    fine_window.geometry("950x450")
    fine_window.config(bg="white")

    # ---------- TITLE ----------
    Label(
        fine_window,
        text="STUDENT FINE RECORDS",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="darkred"
    ).pack(pady=10)

    # ---------- FRAME ----------
    frame = Frame(fine_window)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ---------- SCROLLBARS ----------
    scroll_y = Scrollbar(frame, orient=VERTICAL)
    scroll_x = Scrollbar(frame, orient=HORIZONTAL)

    # ---------- TREEVIEW ----------
    fine_tree = ttk.Treeview(
        frame,
        columns=(
            "Student ID",
            "Book ID",
            "Issue Date",
            "Return Date",
            "Days",
            "Fine"
        ),
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=fine_tree.yview)
    scroll_x.config(command=fine_tree.xview)

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)

    fine_tree.pack(fill=BOTH, expand=True)

    # ---------- HEADINGS ----------
    fine_tree.heading("Student ID", text="Student ID")
    fine_tree.heading("Book ID", text="Book ID")
    fine_tree.heading("Issue Date", text="Issue Date")
    fine_tree.heading("Return Date", text="Return Date")
    fine_tree.heading("Days", text="Days")
    fine_tree.heading("Fine", text="Fine Amount")

    # ---------- COLUMN WIDTH ----------
    fine_tree.column("Student ID", width=120)
    fine_tree.column("Book ID", width=120)
    fine_tree.column("Issue Date", width=120)
    fine_tree.column("Return Date", width=120)
    fine_tree.column("Days", width=80)
    fine_tree.column("Fine", width=100)

    # ---------- DATABASE ----------
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            book_id,
            issue_date,
            return_date
        FROM issued_books
        WHERE return_date IS NOT NULL
    """)

    rows = cursor.fetchall()

    # ---------- CALCULATE FINE ----------
    for row in rows:

        student_id = row[0]
        book_id = row[1]
        issue_date = row[2]
        return_date = row[3]

        # Total days
        cursor.execute(
            "SELECT julianday(?) - julianday(?)",
            (return_date, issue_date)
        )

        days = int(cursor.fetchone()[0])

        # Fine logic
        fine = 0

        if days > 7:
            fine = (days - 7) * 2

        # Insert in table
        fine_tree.insert(
            "",
            END,
            values=(
                student_id,
                book_id,
                issue_date,
                return_date,
                days,
                f"₹{fine}"
            )
        )

    conn.close()