from tkinter import messagebox
import matplotlib.pyplot as plt


# ---------------- SHOW CHART ----------------
def show_chart(connect_db):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(quantity)
    FROM books
    GROUP BY category
    """)

    data = cursor.fetchall()

    conn.close()

    if not data:
        messagebox.showerror(
            "Error",
            "No data available"
        )

        return

    categories = [row[0] for row in data]
    quantities = [row[1] for row in data]

    plt.figure()

    plt.bar(categories, quantities)

    plt.title("Books by Category")
    plt.xlabel("Category")
    plt.ylabel("Quantity")

    plt.show()


# ---------------- FULL DASHBOARD ----------------
def full_dashboard(connect_db):
    conn = connect_db()
    cursor = conn.cursor()

    # CATEGORY DATA
    cursor.execute("""
    SELECT category, SUM(quantity)
    FROM books
    GROUP BY category
    """)

    cat_data = cursor.fetchall()

    categories = [row[0] for row in cat_data]
    quantities = [row[1] for row in cat_data]

    # ISSUED VS AVAILABLE
    cursor.execute("""
    SELECT COUNT(*)
    FROM issued_books
    WHERE return_date IS NULL
    """)

    issued = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(quantity)
    FROM books
    """)

    available = cursor.fetchone()[0]

    if available is None:
        available = 0

    # ISSUE TREND
    cursor.execute("""
    SELECT issue_date, COUNT(*)
    FROM issued_books
    GROUP BY issue_date
    """)

    trend_data = cursor.fetchall()

    dates = [row[0] for row in trend_data]
    counts = [row[1] for row in trend_data]

    conn.close()

    # ===== PLOT =====
    plt.figure()

    # BAR CHART
    plt.subplot(2, 2, 1)

    plt.bar(categories, quantities)

    plt.title("Books by Category")

    # PIE CHART
    plt.subplot(2, 2, 2)

    plt.pie(
        [issued, available],
        labels=["Issued", "Available"],
        autopct='%1.1f%%'
    )

    plt.title("Issued vs Available")

    # LINE CHART
    plt.subplot(2, 1, 2)

    plt.plot(
        dates,
        counts,
        marker='o'
    )

    plt.title("Issue Trend")

    plt.xlabel("Date")
    plt.ylabel("Books Issued")

    plt.tight_layout()

    plt.show()