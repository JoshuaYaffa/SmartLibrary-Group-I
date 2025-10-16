# ================================================
# ReadEasy Mini Library Management System
# ================================================
# PROG211 - Individual Assignment
# Student: Joshua Mohamed Katibi Yaffa
# ID: 905004075
# Class: BSEM1101
# Semester: 3
# Year: 2
# ================================================
# Core Operations Module with Enhanced Features
#
# GitHub: JoshuaYaffa/SmartLibrary-Group-I
# ================================================

"""
This file contains all the main library operations such as adding, updating,
deleting, and searching for books and members. It also manages the borrowing
and returning of books, along with a summary of system activity.
"""

# ==============================
# Data Structures
# ==============================

books = {}      # Stores book details (ISBN -> book info)
members = {}    # Stores member details (ID -> member info)


# ==============================
# Book Management Functions
# ==============================

def add_book(isbn, title, author, genre, total_copies):
    """Adds a new book record into the system."""
    if isbn in books:
        return False
    books[isbn] = {
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        "available_copies": total_copies
    }
    return True


def search_books(keyword):
    """Searches for books by title, author, or genre."""
    results = []
    for book_id, book in books.items():
        if (keyword.lower() in book["title"].lower() or
            keyword.lower() in book["author"].lower() or
            keyword.lower() in book["genre"].lower()):
            results.append((book_id, book))
    return results


def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """Updates existing book details."""
    if isbn not in books:
        return False
    if title:
        books[isbn]["title"] = title
    if author:
        books[isbn]["author"] = author
    if genre:
        books[isbn]["genre"] = genre
    if total_copies is not None:
        difference = total_copies - books[isbn]["total_copies"]
        books[isbn]["total_copies"] = total_copies
        books[isbn]["available_copies"] += difference
        if books[isbn]["available_copies"] < 0:
            books[isbn]["available_copies"] = 0
    return True


def delete_book(isbn):
    """Deletes a book record from the system."""
    if isbn in books:
        del books[isbn]
        return True
    return False


def pretty_print_books():
    """Prints all books in a table-like format."""
    if not books:
        print("No books in the system.")
        return
    print("\n=== List of Books ===")
    print("{:<15} {:<35} {:<25} {:<15} {:<10}".format(
        "ISBN", "Title", "Author", "Genre", "Available"
    ))
    print("-" * 105)
    for book_id, info in books.items():
        print("{:<15} {:<35} {:<25} {:<15} {:<10}".format(
            book_id, info["title"], info["author"], info["genre"], info["available_copies"]
        ))


# ==============================
# Member Management Functions
# ==============================

def add_member(member_id, name, email):
    """Adds a new library member."""
    if member_id in members:
        return False
    members[member_id] = {"name": name, "email": email, "borrowed_books": []}
    return True


def update_member(member_id, name=None, email=None):
    """Updates member information."""
    if member_id not in members:
        return False
    if name:
        members[member_id]["name"] = name
    if email:
        members[member_id]["email"] = email
    return True


def delete_member(member_id):
    """Deletes a member from the system."""
    if member_id in members:
        del members[member_id]
        return True
    return False


def pretty_print_members():
    """Displays all members in a neat table."""
    if not members:
        print("No members found.")
        return
    print("\n=== List of Members ===")
    print("{:<10} {:<30} {:<35} {:<15}".format(
        "ID", "Name", "Email", "Borrowed"
    ))
    print("-" * 100)
    for member_id, info in members.items():
        borrowed = len(info["borrowed_books"])
        print("{:<10} {:<30} {:<35} {:<15}".format(
            member_id, info["name"], info["email"], borrowed
        ))


# ==============================
# Borrow and Return Functions
# ==============================

def borrow_book(isbn, member_id):
    """Allows a member to borrow a book."""
    if isbn not in books or member_id not in members:
        return False
    if books[isbn]["available_copies"] <= 0:
        return False
    if isbn in members[member_id]["borrowed_books"]:
        return False

    books[isbn]["available_copies"] -= 1
    members[member_id]["borrowed_books"].append(isbn)
    return True


def return_book(isbn, member_id):
    """Allows a member to return a borrowed book."""
    if isbn not in books or member_id not in members:
        return False
    if isbn not in members[member_id]["borrowed_books"]:
        return False

    books[isbn]["available_copies"] += 1
    members[member_id]["borrowed_books"].remove(isbn)
    return True


# ==============================
# System Summary
# ==============================

def system_summary():
    """Displays a summary of total books, members, and borrowed books."""
    total_books = len(books)
    total_members = len(members)
    borrowed_books = sum(
        len(member["borrowed_books"]) for member in members.values()
    )

    print("\n=== System Summary ===")
    print(f"Total Books: {total_books}")
    print(f"Total Members: {total_members}")
    print(f"Total Books Borrowed: {borrowed_books}")


# ==============================
# Preloaded Data for Demonstration
# ==============================

# Preloaded Books
sample_books = [
    ("91", "Harry Potter and the Goblet of Fire", "J.K. Rowling", "Fantasy", 10),
    ("92", "The Odyssey", "Homer", "Epic", 5),
    ("93", "To Kill a Mockingbird", "Harper Lee", "Fiction", 8),
    ("94", "The Kite Runner", "Khaled Hosseini", "Drama", 6),
    ("95", "The Great Gatsby", "F. Scott Fitzgerald", "Classic", 7),
    ("96", "Fahrenheit 451", "Ray Bradbury", "Science Fiction", 9),
    ("97", "Dune", "Frank Herbert", "Sci-Fi", 12),
    ("98", "The Catcher in the Rye", "J.D. Salinger", "Classic", 5),
    ("99", "It Ends With Us", "Colleen Hoover", "Romance", 10),
    ("100", "Harry Potter and the Deathly Hallows", "J.K. Rowling", "Fantasy", 11)
]

for isbn, title, author, genre, copies in sample_books:
    if isbn not in books:
        books[isbn] = {
            "title": title,
            "author": author,
            "genre": genre,
            "total_copies": copies,
            "available_copies": copies
        }

# Preloaded Members
sample_members = [
    ("M001", "Joshua Mohamed Katibi Yaffa", "joshua.yaffa@example.com"),
    ("M002", "Sarah Conteh", "sarah.conteh@example.com"),
    ("M003", "Mohamed Kamara", "mohamed.kamara@example.com"),
    ("M004", "Abigail Koroma", "abigail.koroma@example.com"),
    ("M005", "David Sesay", "david.sesay@example.com"),
    ("M006", "Fatmata Jalloh", "fatmata.jalloh@example.com"),
    ("M007", "Josephine Mansaray", "josephine.mansaray@example.com"),
    ("M008", "Alhassan Bangura", "alhassan.bangura@example.com"),
    ("M009", "Mariatu Kargbo", "mariatu.kargbo@example.com"),
    ("M010", "Isata Conteh", "isata.conteh@example.com")
]

for member_id, name, email in sample_members:
    if member_id not in members:
        members[member_id] = {
            "name": name,
            "email": email,
            "borrowed_books": []
        }
