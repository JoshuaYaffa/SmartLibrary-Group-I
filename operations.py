# ================================================
# ReadEasy Mini Library Management System
#
# PROG211 - Individual Assignment
# Student: Joshua Mohamed Katibi Yaffa
# ID: 905004075
# Class: BSEM1101
# Semester: 3
# Year: 2
#
# Core Operations Module with Enhanced Features
#
# GitHub: JoshuaYaffa/SmartLibrary-Group-I
# ================================================

"""
This file contains all the core operations for my Mini Library Management System.
It handles the CRUD operations for books and members, as well as the borrow and return functions.
I have also linked it with the security.py file for logging, auditing and tracking user actions.

"""

from security import log_event, current_user, log_error
import re

# I am using global variables to store all data in memory
books = {}        # Dictionary for all books (key = ISBN)
members = []      # List to hold all member information
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Children", "Academic")


# ==============================
# Helper Functions
# ==============================

def _is_valid_email(email):
    """
    This function checks if the email entered is valid.
    I used a simple regex pattern to confirm the email structure.
    """
    if not isinstance(email, str):
        return False
    email = email.strip()
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email) is not None


def _find_member(member_id):
    """
    This function searches for a member in the list using their ID.
    It returns the member dictionary if found, otherwise None.
    """
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None


def _is_isbn_unique(isbn):
    """Checks that a book ISBN does not already exist."""
    return isbn not in books


# ==============================
# Book Operations
# ==============================

def add_book(isbn, title, author, genre, total_copies):
    """
    Adds a new book to the system.
    It checks if the ISBN is unique, genre is valid, and copies > 0 before adding.
    """
    try:
        if not isbn or not title or not author:
            return False
        if not _is_isbn_unique(isbn):
            return False
        if genre not in GENRES:
            return False
        if not isinstance(total_copies, int) or total_copies <= 0:
            return False
        books[isbn] = {
            "title": title.strip(),
            "author": author.strip(),
            "genre": genre,
            "total_copies": total_copies
        }
        if current_user:
            log_event(current_user["username"], f"Added book: {title} (ISBN: {isbn})")
        return True
    except Exception as e:
        log_error(str(e))
        return False


def search_books(query, by="title"):
    """
    Searches for books in the system by title or author.
    The search is case-insensitive and allows partial matches.
    """
    results = []
    if not query:
        return results
    q = query.strip().lower()
    for isbn, book in books.items():
        if by == "author":
            if q in book["author"].lower():
                results.append((isbn, book))
        else:
            if q in book["title"].lower():
                results.append((isbn, book))
    return results


def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """
    Updates details of a book if it already exists.
    I used optional parameters so that only the given fields are updated.
    """
    try:
        book = books.get(isbn)
        if not book:
            return False
        if genre is not None and genre not in GENRES:
            return False
        if total_copies is not None:
            if not isinstance(total_copies, int) or total_copies < 0:
                return False
            book["total_copies"] = total_copies
        if title is not None:
            book["title"] = title.strip()
        if author is not None:
            book["author"] = author.strip()
        if genre is not None:
            book["genre"] = genre
        if current_user:
            log_event(current_user["username"], f"Updated book: {isbn}")
        return True
    except Exception as e:
        log_error(str(e))
        return False


def delete_book(isbn):
    """
    Deletes a book only if it exists and is not currently borrowed by anyone.
    """
    try:
        if isbn not in books:
            return False
        for member in members:
            if isbn in member["borrowed_books"]:
                return False
        title = books[isbn]["title"]
        del books[isbn]
        if current_user:
            log_event(current_user["username"], f"Deleted book: {title} (ISBN: {isbn})")
        return True
    except Exception as e:
        log_error(str(e))
        return False


# ==============================
# Member Operations
# ==============================

def add_member(member_id, name, email):
    """
    Adds a new member to the library.
    Before adding, I checked that:
      - The ID is unique
      - The email format is valid
      - The email is not already used by another member
    """
    try:
        if not member_id or not name or not email:
            return False
        if _find_member(member_id):
            return False
        if not _is_valid_email(email):
            return False
        for existing_member in members:
            if existing_member["email"].strip().lower() == email.strip().lower():
                return False
        new_member = {
            "member_id": member_id,
            "name": name.strip(),
            "email": email.strip(),
            "borrowed_books": []
        }
        members.append(new_member)
        if current_user:
            log_event(current_user["username"], f"Added member: {name} (ID: {member_id})")
        return True
    except Exception as e:
        log_error(str(e))
        return False


def update_member(member_id, name=None, email=None):
    """
    Updates an existing member's details.
    I made sure emails are validated and not duplicated for other members.
    """
    try:
        member = _find_member(member_id)
        if not member:
            return False
        if email is not None:
            if not _is_valid_email(email):
                return False
            for other_member in members:
                if other_member["member_id"] != member_id and other_member["email"].strip().lower() == email.strip().lower():
                    return False
            member["email"] = email.strip()
        if name is not None:
            member["name"] = name.strip()
        if current_user:
            log_event(current_user["username"], f"Updated member: {member_id}")
        return True
    except Exception as e:
        log_error(str(e))
        return False


def delete_member(member_id):
    """
    Deletes a member only if they exist and currently have no borrowed books.
    """
    try:
        member = _find_member(member_id)
        if not member:
            return False
        if member["borrowed_books"]:
            return False
        members.remove(member)
        if current_user:
            log_event(current_user["username"], f"Deleted member: {member_id}")
        return True
    except Exception as e:
        log_error(str(e))
        return False


# ==============================
# Borrowing and Returning
# ==============================

def borrow_book(isbn, member_id):
    """
    Allows a member to borrow a book if:
      - The book exists and is available
      - The member exists
      - The member has borrowed less than 3 books
    """
    try:
        book = books.get(isbn)
        if not book:
            return False
        if book["total_copies"] <= 0:
            return False
        member = _find_member(member_id)
        if not member:
            return False
        if len(member["borrowed_books"]) >= 3:
            return False
        if isbn in member["borrowed_books"]:
            return False
        book["total_copies"] -= 1
        member["borrowed_books"].append(isbn)
        if current_user:
            log_event(current_user["username"], f"Borrowed book: {book['title']} (ISBN: {isbn}) for member {member_id}")
        return True
    except Exception as e:
        log_error(str(e))
        return False


def return_book(isbn, member_id):
    """
    Allows a member to return a borrowed book.
    Once returned, total_copies increases and the book is removed from their borrowed list.
    """
    try:
        book = books.get(isbn)
        if not book:
            return False
        member = _find_member(member_id)
        if not member:
            return False
        if isbn not in member["borrowed_books"]:
            return False
        member["borrowed_books"].remove(isbn)
        book["total_copies"] += 1
        if current_user:
            log_event(current_user["username"], f"Returned book: {book['title']} (ISBN: {isbn}) by member {member_id}")
        return True
    except Exception as e:
        log_error(str(e))
        return False


# ==============================
# Utility Functions
# ==============================

def system_summary():
    """
    Displays a short summary of the system including:
    - Total books
    - Total members
    - Total borrowed copies
    """
    total_books = len(books)
    total_members = len(members)
    total_borrowed = sum(len(member["borrowed_books"]) for member in members)
    print("\n=== System Summary ===")
    print(f"Total distinct books: {total_books}")
    print(f"Total members: {total_members}")
    print(f"Total borrowed copies (across members): {total_borrowed}")
    print("======================\n")


def pretty_print_books():
    """
    Prints out all the books in a readable format.
    Each book record shows title, author, genre, and available copies.
    """
    if not books:
        print("No books in the system.")
        return
    print("\n=== Books ===")
    for isbn, book in books.items():
        print(f"ISBN: {isbn} | Title: {book['title']} | Author: {book['author']} | Genre: {book['genre']} | Available copies: {book['total_copies']}")
    print("=============\n")


def pretty_print_members():
    """
    Prints out all members in the system.
    Each member’s borrowed books are also shown.
    """
    if not members:
        print("No members in the system.")
        return
    print("\n=== Members ===")
    for member in members:
        print(f"ID: {member['member_id']} | Name: {member['name']} | Email: {member['email']} | Borrowed: {member['borrowed_books']}")
    print("================\n")
