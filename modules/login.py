from tkinter import *
from tkinter import messagebox


# ---------------- LOGIN WINDOW ----------------
def open_login(root):
    login = Toplevel()

    login.title("Admin Login")
    login.geometry("400x300")

    login.config(bg="#d9f0ff")

    Label(
        login,
        text="SMART LIBRARY LOGIN",
        font=("Arial", 18, "bold"),
        bg="#d9f0ff",
        fg="darkblue"
    ).pack(pady=20)

    Label(
        login,
        text="Username",
        bg="#d9f0ff"
    ).pack()

    username_entry = Entry(login)
    username_entry.pack()

    Label(
        login,
        text="Password",
        bg="#d9f0ff"
    ).pack()

    password_entry = Entry(
        login,
        show="*"
    )

    password_entry.pack()

    def check_login():
        if (
            username_entry.get() == "ankita"
            and
            password_entry.get() == "admin123"
        ):
            login.destroy()
            root.deiconify()

        else:
            messagebox.showerror(
                "Error",
                "Invalid login"
            )

    Button(
        login,
        text="Login",
        command=check_login
    ).pack(pady=20)