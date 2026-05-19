from tkinter import messagebox


# ---------------- AUTO ADD BOOKS ----------------
def auto_add_books(
    connect_db,
    view_books_function,
    update_stats_function
):
    conn = connect_db()
    cursor = conn.cursor()

    books = [
        ("P101", "Python Basics", "Guido van Rossum", "Computer", 5),
        ("P102", "Java Programming", "James Gosling", "Computer", 5),
        ("P103", "C++ Guide", "Bjarne Stroustrup", "Computer", 5),
        ("P104", "DBMS Concepts", "Navathe", "Computer", 5),
        ("P105", "Web Development", "Mozilla Team", "Computer", 5),

        ("S201", "Physics Today", "Albert Einstein", "Science", 5),
        ("S202", "Chemistry World", "Marie Curie", "Science", 5),
        ("S203", "Biology Basics", "Charles Darwin", "Science", 5),
        ("S204", "Space Science", "Various Authors", "Science", 5),
        ("S205", "Human Body", "Medical Experts", "Science", 5),

        ("N301", "Harry Potter", "J.K. Rowling", "Novel", 5),
        ("N302", "The Alchemist", "Paulo Coelho", "Novel", 5),
        ("N303", "Sherlock Holmes", "Arthur Conan Doyle", "Novel", 5),
        ("N304", "The Hobbit", "J.R.R. Tolkien", "Novel", 5),
        ("N305", "Pride and Prejudice", "Jane Austen", "Novel", 5),

        # Fairy Tale
        ("F401", "Cinderella", "Various Authors", "Fairy Tale", 5, ),
        ("F402", "Snow White", "Brothers Grimm", "Fairy Tale", 5, ),
        ("F403", "Rapunzel", "Brothers Grimm", "Fairy Tale", 5, ),
        ("F404", "Sleeping Beauty", "Various Authors", "Fairy Tale", 5, ),
        ("F405", "Little Red Riding Hood", "Brothers Grimm", "Fairy Tale", 5, ),
        # History
        ("H501", "World History", "Various Authors", "History", 5, ),
        ("H502", "Ancient India", "Historians", "History", 5, ),
        ("H503", "Freedom Struggle", "Indian Authors", "History", 5, ),
        ("H504", "Modern History", "Scholars", "History", 5, ),
        ("H505", "World Wars", "Historians", "History", 5, ),
        # Biography
        ("B601", "Wings of Fire", "A.P.J. Abdul Kalam", "Biography", 5, ),
        ("B602", "Steve Jobs", "Walter Isaacson", "Biography", 5, ),
        ("B603", "Einstein Life", "Various Authors", "Biography", 5, ),
        ("B604", "Gandhi Biography", "Various Authors", "Biography", 5, ),
        ("B605", "Lincoln Life", "Various Authors", "Biography", 5, ),
        # Philosophy
        ("PH701", "Republic", "Plato", "Philosophy", 5, ),
        ("PH702", "Meditations", "Marcus Aurelius", "Philosophy", 5, ),
        ("PH703", "Beyond Good and Evil", "Nietzsche", "Philosophy", 5, ),
        # Self-Help
        ("SH801", "Think and Grow Rich", "Napoleon Hill", "Self-Help", 5, ),
        ("SH802", "Atomic Habits", "James Clear", "Self-Help", 5, ),
        ("SH803", "The Power of Now", "Eckhart Tolle", "Self-Help", 5, ),
        # Poetry
        ("PO901", "Leaves of Grass", "Walt Whitman", "Poetry", 5, ),
        ("PO902", "Gitanjali", "Rabindranath Tagore", "Poetry", 5, ),
        ("PO903", "The Waste Land", "T.S. Eliot", "Poetry", 5, ),
        # Business
        ("BU1001", "Rich Dad Poor Dad", "Robert Kiyosaki", "Business", 5, ),
        ("BU1002", "The Lean Startup", "Eric Ries", "Business", 5, ),
        ("BU1003", "Zero to One", "Peter Thiel", "Business", 5, ),
        # Travel
        ("TR1101", "Lonely Planet India", "Lonely Planet", "Travel", 5, ),
        ("TR1102", "Around the World in 80 Days", "Jules Verne", "Travel", 5, ),
        # Children
        ("CH1201", "The Cat in the Hat", "Dr. Seuss", "Children", 5, ),
        ("CH1202", "Alice in Wonderland", "Lewis Carroll", "Children", 5, ),
        # Technology
        ("T1301", "Artificial Intelligence", "Stuart Russell", "Technology", 5, ),
        ("T1302", "Clean Code", "Robert C. Martin", "Technology", 5, ),
        ("T1303", "Introduction to Algorithms", "Cormen et al.", "Technology", 5, ),
        # Mathematics  
        ("M1401", "Linear Algebra", "Gilbert Strang", "Mathematics", 5, ),
        ("M1402", "Calculus Made Easy", "Silvanus P. Thompson", "Mathematics", 5, ),
        ("M1403", "Discrete Mathematics", "Kenneth Rosen", "Mathematics", 5, ),
        ("M1404", "Probability Theory", "Sheldon Ross", "Mathematics", 5, ),
        ("M1405", "Number Theory", "G.H. Hardy", "Mathematics", 5, ),  
        # Psychology
        ("PS1501", "Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 5, ),
        ("PS1502", "Man's Search for Meaning", "Viktor Frankl", "Psychology", 5, ),
        ("PS1503", "The Power of Habit", "Charles Duhigg", "Psychology", 5, ),
        ("PS1504", "Influence", "Robert Cialdini", "Psychology", 5, ),
        ("PS1505", "Emotional Intelligence", "Daniel Goleman", "Psychology", 5, ),
        # Geography
        ("G1601", "World Atlas", "National Geographic", "Geography", 5, ),
        ("G1602", "Physical Geography", "Savindra Singh", "Geography", 5, ),
        ("G1603", "Indian Geography", "Majid Husain", "Geography", 5, ),
        ("G1604", "Climate Change", "Various Authors", "Geography", 5, ),
        ("G1605", "Oceanography Basics", "Marine Scientists", "Geography", 5, ),
        # Arts & Design
        ("A1801", "Fundamentals of Drawing", "Andrew Loomis", "Arts", 5, ),
        ("A1802", "Color Theory", "Johannes Itten", "Arts", 5, ),
        ("A1803", "Digital Painting Basics", "Concept Artists", "Arts", 5,  ),
        ("A1804", "Art History", "E.H. Gombrich", "Arts", 5, ),
        ("A1805", "Sketching for Beginners", "Art Tutors", "Arts", 5, ),
        # Finance & Economics
        ("F1901", "Economics Basics", "Paul Samuelson", "Finance", 5, ),
        ("F1902", "The Intelligent Investor", "Benjamin Graham", "Finance", 5, ),
        ("F1903", "Money Psychology", "Morgan Housel", "Finance", 5, ),
        ("F1904", "Macroeconomics", "N. Gregory Mankiw", "Finance", 5, ),
        ("F1905", "Personal Finance Guide", "Various Authors", "Finance", 5, ),
        # Mystery / Thriller
        ("MY2001", "Gone Girl", "Gillian Flynn", "Mystery", 5, ),
        ("MY2002", "Da Vinci Code", "Dan Brown", "Mystery", 5, ),
        ("MY2003", "And Then There Were None", "Agatha Christie", "Mystery", 5, ),
        ("MY2004", "The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery", 5, ),
        ("MY2005", "Shutter Island", "Dennis Lehane", "Mystery", 5, ),
        # Laws & Legal Studies
        ("L2101", "Constitution of India", "Dr. B.R. Ambedkar", "Law", 5, ),
        ("L2102", "Introduction to Law", "S.N. Dhingra", "Law", 5, ),
        ("L2103", "Criminal Law Basics", "Legal Experts", "Law", 5, ),
        ("L2104", "Human Rights Law", "UN Publications", "Law", 5, ),
        ("L2105", "Cyber Law in India", "Legal Scholars", "Law", 5, ),
        # Health & Fitness
        ("HF2201", "Yoga for Beginners", "B.K.S. Iyengar", "Health", 5, ),
        ("HF2202", "Fitness Anatomy", "Arnold Schwarzenegger", "Health", 5, ),
        ("HF2203", "Healthy Living Guide", "WHO Experts", "Health", 5, ),
        ("HF2204", "Nutrition Basics", "Diet Experts", "Health", 5, ),
        ("HF2205", "Mental Wellness", "Psychology Experts", "Health", 5, ),
        # Engineering
        ("E2301", "Mechanical Engineering Basics", "Engineering Authors", "Engineering", 5, ),
        ("E2302", "Electrical Circuits", "Alexander Sadiku", "Engineering", 5, ),
        ("E2303", "Civil Engineering Handbook", "Civil Experts", "Engineering", 5, ),
        ("E2304", "Thermodynamics", "Yunus Çengel", "Engineering", 5, ),
        ("E2305", "Engineering Mathematics", "B.S. Grewal", "Engineering", 5, ),
        # Mythology
        ("MYT2401", "Ramayana", "Valmiki", "Mythology", 5, ),
        ("MYT2402", "Mahabharata", "Vyasa", "Mythology", 5, ),
        ("MYT2403", "Greek Mythology Stories", "Ancient Writers", "Mythology", 5, ),
        ("MYT2404", "Norse Mythology", "Neil Gaiman", "Mythology", 5, ),
        ("MYT2405", "Egyptian Gods", "Historians", "Mythology", 5, ),
        # Sports
        ("SP2501", "Cricket History", "Sports Authors", "Sports", 5, ),
        ("SP2502", "Football Guide", "FIFA Experts", "Sports", 5, ),
        ("SP2503", "Olympic Games History", "IOC", "Sports", 5, ),
        ("SP2504", "Sports Science", "Athletic Trainers", "Sports", 5, ),
        ("SP2505", "Training and Diet for Athletes", "Fitness Coaches", "Sports", 5, ),
        # Music
        ("MU2601", "Basics of Music Theory", "Music Experts", "Music", 5, ),
        ("MU2602", "Indian Classical Music", "Pandit Ravi Shankar", "Music", 5, ),
        ("MU2603", "Western Music History", "Music Scholars", "Music", 5, ),
        ("MU2604", "Guitar for Beginners", "Music Tutors", "Music", 5, ),
        ("MU2605", "Piano Guide", "Classical Musicians", "Music", 5, ),
        # Entrepreneurship 
        ("EN2701", "Startup Guide", "Entrepreneurs", "Entrepreneurship", 5, ),
        ("EN2702", "Business Ideas", "Startup Mentors", "Entrepreneurship", 5, ),
        ("EN2703", "Innovation Thinking", "Steve Jobs Influence", "Entrepreneurship", 5, ),
        ("EN2704", "How to Build a Company", "Elon Musk Inspiration", "Entrepreneurship", 5, ),
        ("EN2705", "Marketing Strategies", "Philip Kotler", "Entrepreneurship", 5, ),
    ]

    try:
        cursor.executemany("""
        INSERT OR IGNORE INTO books VALUES(?,?,?,?,?)
        """, books)

        conn.commit()

        view_books_function()
        update_stats_function()

        messagebox.showinfo(
            "Success",
            "Books Added Successfully!"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

    finally:
        conn.close()