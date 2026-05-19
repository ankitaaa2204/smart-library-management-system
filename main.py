
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from modules.database import connect_db, create_tables
from modules.utils import update_stats, clear_fields, select_row
from modules.book_operations import (add_book,view_books,search_book,delete_book,update_book)
from modules.student_operations import add_student
from modules.issue_return import (issue_book,return_book,calculate_fine)
from modules.reports import (show_dashboard,export_to_excel)
from modules.charts import (show_chart,full_dashboard)
from modules.auto_books import auto_add_books
from modules.login import open_login
from modules.windows import show_issued_books,show_students,show_student_fines
        
#==================== Auto Book Generator ====================
import random
def generate_books():
    conn = connect_db()
    cursor = conn.cursor()
    titles = {
        "Computer": ["Python Basics", "Java Advanced", "C++ Mastery", "DBMS Guide", "Web Development"],
        "Science": ["Physics World", "Chemistry Lab", "Biology Basics", "Space Science", "Human Anatomy"],
        "Novel": ["Great Expectations", "The Alchemist", "Sherlock Holmes", "The Hobbit", "Invisible Man"],
        "History": ["World History", "Ancient India", "Modern History", "Freedom Struggle", "World Wars"],
        "Business": ["Rich Dad Poor Dad", "Lean Startup", "Zero to One", "Business Strategy", "Marketing 101"]
    }
    authors = [
        "Author A", "Author B", "Author C", "Author D", "Author E"
    ]
    books = []
    counter = 1000
    for category, title_list in titles.items():
        for title in title_list:
            book_id = f"{category[:2].upper()}{counter}"
            author = random.choice(authors)

            books.append((book_id, title, author, category, 5))
            counter += 1
    try:
        cursor.executemany("""INSERT OR IGNORE INTO books(book_id, title, author, category, quantity)VALUES (?,?,?,?,?)
        """, books)
        conn.commit()
        messagebox.showinfo("Success", "Books Generated Automatically!")
        view_books()
        update_stats_wrapper()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

# ==================== THEME ====================
def set_light_mode():

    root.config(bg="lightblue")

    frame.config(bg="lightblue")
    btn_frame.config(bg="lightblue")
    search_frame.config(bg="lightblue")

    title_count_label.config(bg="lightblue", fg="black")
    qty_count_label.config(bg="lightblue", fg="black")

    title_label.config(bg="lightblue", fg="darkblue")

    for widget in frame.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg="lightblue", fg="black")

    for widget in btn_frame.winfo_children():
        if isinstance(widget, Button):
            widget.config(bg="white", fg="black")

    exit_button.config(bg="red", fg="white")

def set_dark_mode():

    root.config(bg="#1e1e1e")

    frame.config(bg="#1e1e1e")
    btn_frame.config(bg="#1e1e1e")
    search_frame.config(bg="#1e1e1e")

    title_count_label.config(bg="#1e1e1e", fg="white")
    qty_count_label.config(bg="#1e1e1e", fg="white")

    title_label.config(bg="#1e1e1e", fg="#00bfff")

    for widget in frame.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg="#1e1e1e", fg="white")

    for widget in btn_frame.winfo_children():
        if isinstance(widget, Button):
            widget.config(bg="#333333", fg="white")

    exit_button.config(bg="red", fg="white")

# =====================EXIT APPLICATION===================
def exit_app():
    confirm = messagebox.askyesno(
        "Exit",
        "Do you really want to exit?"
    )
    if confirm:
        root.destroy()

# ==================== SPLASH SCREEN ======================
def show_splash():
    splash = Toplevel()
    splash.title("Loading")
    splash.geometry("500x300")
    splash.configure(bg="#1e3d59")
    splash.overrideredirect(True)

    # Center splash
    width = 500
    height = 300
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    splash.geometry(f"{width}x{height}+{x}+{y}")

    Label(
        splash,
        text="SMART LIBRARY MANAGEMENT SYSTEM",
        font=("Arial", 20, "bold"),
        bg="#1e3d59",
        fg="white"
    ).pack(expand=True)
    Label(
        splash,
        text="Loading Application...",
        font=("Arial", 12),
        bg="#1e3d59",
        fg="white"
    ).pack(pady=20)
    def close_splash():
        splash.destroy()
        open_login_wrapper()
    splash.after(2500, close_splash)
    return 

# ==================== UTILITY WRAPPERS ====================
def update_stats_wrapper():
    update_stats(
        connect_db,
        title_count_label,
        qty_count_label
    )

def clear_fields_wrapper():
    clear_fields(
        entry_id,
        entry_title,
        entry_author,
        entry_category,
        entry_quantity,
        student_entry,
        student_id_entry,
        student_name_entry,
        student_course_entry
    )

def select_row_wrapper(event):
    select_row(
        event,
        tree,
        clear_fields_wrapper,
        entry_id,
        entry_title,
        entry_author,
        entry_category,
        entry_quantity
    )

# ===================== BOOK OPERATION WRAPPERS ====================
def view_books_wrapper():
    view_books(connect_db, tree)

def search_book_wrapper():
    search_book(connect_db, tree, search_entry)

def add_book_wrapper():
    add_book(
        connect_db,
        entry_id,
        entry_title,
        entry_author,
        entry_category,
        entry_quantity,
        clear_fields_wrapper,
        view_books_wrapper,
        update_stats_wrapper
    )

def delete_book_wrapper():
    delete_book(
        connect_db,
        tree,
        clear_fields_wrapper,
        view_books_wrapper,
        update_stats_wrapper
    )

def update_book_wrapper():
    update_book(
        connect_db,
        entry_id,
        entry_title,
        entry_author,
        entry_category,
        entry_quantity,
        clear_fields_wrapper,
        view_books_wrapper,
        update_stats_wrapper
    )

# ================ STUDENT WRAPPERS ================
def add_student_wrapper():
    add_student(
        connect_db,
        student_id_entry,
        student_name_entry,
        student_course_entry
    )

# ================== ISSUE/RETURN WRAPPERS ==================
def issue_book_wrapper():
    issue_book(
        connect_db,
        entry_id,
        student_id_entry,
        view_books_wrapper,
        update_stats_wrapper
    )

def return_book_wrapper():
    return_book(
        connect_db,
        entry_id,
        student_id_entry,
        view_books_wrapper,
        update_stats_wrapper
    )

def calculate_fine_wrapper():
    calculate_fine(connect_db)

# =================== REPORT WRAPPERS ==================
def show_dashboard_wrapper():
    show_dashboard(connect_db)

def export_excel_wrapper():
    export_to_excel(connect_db)

# =================== CHART WRAPPERS ==================
def show_chart_wrapper():
    show_chart(connect_db)

def full_dashboard_wrapper():
    full_dashboard(connect_db)

# =================== AUTO BOOK WRAPPER ===================
def auto_add_books_wrapper():
    auto_add_books(
        connect_db,
        view_books_wrapper,
        update_stats_wrapper
    )

# ================== LOGIN WRAPPER ==================
def open_login_wrapper():
    open_login(root)

# =====================GUI=====================
create_tables()
root = Tk()
root.withdraw()
root.title("Smart Library Management System")
root.geometry("900x700")
root.config(bg="lightblue")
root.protocol("WM_DELETE_WINDOW", exit_app)

# ===================LOGO===================
try:
    img = Image.open("logo.png")
    img = img.resize((80, 80))
    logo = ImageTk.PhotoImage(img)
    logo_label = Label(root, image=logo, bg="lightblue")
    logo_label.image = logo
    logo_label.pack(pady=5)
except:
    Label(
        root,
        text="📚",
        font=("Arial", 40),
        bg="lightblue"
    ).pack(pady=5)

# ===================TITLE===================
title_label = Label(
    root,
    text="SMART LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="lightblue",
    fg="darkblue"
)
title_label.pack(pady=10)
title_count_label = Label(root, text="Total Titles: 0", bg="lightblue")
title_count_label.pack()

qty_count_label = Label(root, text="Total Books: 0/3000", bg="lightblue")
qty_count_label.pack()

frame = Frame(root, bg="lightblue")
frame.pack()
  

entry_id = Entry(frame)
entry_title = Entry(frame)
entry_author = Entry(frame)
entry_category = Entry(frame)
entry_quantity = Entry(frame)

# ===================FORM===================
Label(frame, text="Book ID", bg="lightblue").grid(row=0, column=0)
entry_id.grid(row=0, column=1)
Label(frame, text="Title", bg="lightblue").grid(row=1, column=0)
entry_title.grid(row=1, column=1)
Label(frame, text="Author", bg="lightblue").grid(row=2, column=0)
entry_author.grid(row=2, column=1)
Label(frame, text="Category", bg="lightblue").grid(row=3, column=0)
entry_category.grid(row=3, column=1)
Label(frame, text="Quantity", bg="lightblue").grid(row=4, column=0)
entry_quantity.grid(row=4, column=1)

# -------- STUDENT SECTION --------
Label(frame, text="Student ID", bg="lightblue").grid(row=5, column=0)
student_id_entry = Entry(frame)
student_id_entry.grid(row=5, column=1)
Label(frame, text="Student Name", bg="lightblue").grid(row=6, column=0)
student_name_entry = Entry(frame)
student_name_entry.grid(row=6, column=1)
Label(frame, text="Course", bg="lightblue").grid(row=7, column=0)
student_course_entry = Entry(frame)
student_course_entry.grid(row=7, column=1)

# -------- ISSUE SECTION --------
Label(frame, text="Issue Student Name", bg="lightblue").grid(row=8, column=0)
student_entry = Entry(frame)
student_entry.grid(row=8, column=1)

# ---------------- BUTTON FRAME ----------------
btn_frame = Frame(root, bg="lightblue")
btn_frame.pack(pady=10)
# Row 1 (Book operations)
Button(btn_frame, text="Add Book", width=15, command=add_book_wrapper).grid(row=0, column=0, padx=5, pady=5)
Button(btn_frame, text="View Books", width=15, command=view_books_wrapper).grid(row=0, column=1, padx=5, pady=5)
Button(btn_frame, text="Update Book", width=15, command=update_book_wrapper).grid(row=0, column=2, padx=5, pady=5)
Button(btn_frame, text="Delete Book", width=15, command=delete_book_wrapper).grid(row=0, column=3, padx=5, pady=5)
# Row 2 (Student + Auto)
Button(btn_frame, text="Add Student", width=15, command=add_student_wrapper).grid(row=1, column=0, padx=5, pady=5)
Button(btn_frame, text="Student Records", width=15, command=show_students).grid(row=1, column=1, padx=5, pady=5)
Button(btn_frame, text="Auto Add Books", width=15, command=auto_add_books_wrapper).grid(row=1, column=2, padx=5, pady=5)
Button(btn_frame, text="Issue Book", width=15, command=issue_book_wrapper).grid(row=1, column=3, padx=5, pady=5)
Button(btn_frame, text="Return Book", width=15, command=return_book_wrapper).grid(row=1, column=4, padx=5, pady=5)
# Row 3 (Reports)
Button(btn_frame, text="Calculate Fine", width=15, command=calculate_fine_wrapper).grid(row=2, column=0, padx=5, pady=5)
Button(btn_frame, text="Student Fine", width=15, command=show_student_fines).grid(row=2, column=1, padx=5, pady=5)
Button(btn_frame, text="Show Chart", width=15, command=show_chart_wrapper).grid(row=2, column=2, padx=5, pady=5)
Button(btn_frame, text="Full Dashboard", width=15, command=full_dashboard_wrapper).grid(row=2, column=3, padx=5, pady=5)
Button(btn_frame, text="Export Excel", width=15, command=export_excel_wrapper).grid(row=2, column=4, padx=5, pady=5)
Button(btn_frame, text="Issued Books", width=15, command=show_issued_books).grid(row=3, column=0, padx=5, pady=5)
Button(btn_frame, text="Dark Mode", width=15, command=set_dark_mode).grid(row=3, column=1, padx=5, pady=5)
Button(btn_frame, text="Light Mode", width=15, command=set_light_mode).grid(row=3, column=2, padx=5, pady=5)
# Row 4(Exit)
Button(root, text="Auto Generate Books", command=generate_books).pack()
exit_button = Button(btn_frame, text="Exit", width=15, command=exit_app, bg="red", fg="white")
exit_button.grid(row=4, column=0, columnspan=2, pady=10)

# ---------------- SEARCH FRAME ----------------
search_frame = Frame(root, bg="lightblue")
search_frame.pack(pady=10)
search_entry = Entry(search_frame, width=30)
search_entry.grid(row=0, column=0, padx=5)
Button(search_frame, text="Search", command=search_book_wrapper).grid(row=0, column=1)
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=28,
    fieldbackground="white",
    font=("Arial", 10)
)
style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold"),
    background="#007ACC",
    foreground="white"
)

# =============  TREEVIEW + SCROLLBAR ================

tree_frame = Frame(root)
tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

tree = ttk.Treeview(
    tree_frame,
    columns=("ID", "Title", "Author", "Category", "Qty"),
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set,
    height=18
)
scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)

tree.pack(fill=BOTH, expand=True)

tree.heading("ID", text="Book ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.heading("Category", text="Category")
tree.heading("Qty", text="Quantity")

tree.column("ID", width=150)
tree.column("Title", width=350)
tree.column("Author", width=250)
tree.column("Category", width=180)
tree.column("Qty", width=120)

tree.bind("<ButtonRelease-1>", select_row_wrapper)
view_books_wrapper()
update_stats_wrapper()
root.after(100, show_splash)
root.mainloop()
