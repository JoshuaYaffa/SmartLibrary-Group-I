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
# Test Module for Core Functionalities
#
# GitHub: JoshuaYaffa/SmartLibrary-Group-I
# ================================================

"""
This file contains my test cases for the ReadEasy Mini Library Management System.
I used simple assert statements to check that all my main functions in operations.py
are working correctly. Each section tests a different part of the system.
"""

from operations import (
    add_book, search_books, update_book, delete_book,
    add_member, update_member, delete_member,
    borrow_book, return_book, books, members
)


def run_all_tests():
    """
    This function runs all my tests in order.
    If all tests pass, I will print a success message at the end.
    """

    # ==========================================
    # 1. Test Adding Books
    # ==========================================
    print("Testing add_book()...")
    assert add_book("B001", "Python Basics", "John Smith", "Academic", 3) == True
    assert add_book("B001", "Duplicate ISBN", "Another Author", "Fiction", 2) == False
    assert add_book("B002", "Story Time", "James Doe", "Fiction", 5) == True
    print("Book addition tests passed.")

    # ==========================================
    # 2. Test Searching Books
    # ==========================================
    print("Testing search_books()...")
    result = search_books("python")
    assert len(result) == 1
    assert result[0][1]["title"] == "Python Basics"
    print("Book search tests passed.")

    # ==========================================
    # 3. Test Updating Books
    # ==========================================
    print("Testing update_book()...")
    assert update_book("B001", title="Python for Everyone") == True
    assert books["B001"]["title"] == "Python for Everyone"
    assert update_book("B999", title="Unknown Book") == False
    print("Book update tests passed.")

    # ==========================================
    # 4. Test Adding Members
    # ==========================================
    print("Testing add_member()...")
    assert add_member("M001", "Alice Johnson", "alice@example.com") == True
    assert add_member("M001", "Duplicate ID", "alice2@example.com") == False
    assert add_member("M002", "Bob Brown", "bob@example.com") == True
    print("Member addition tests passed.")

    # ==========================================
    # 5. Test Updating Members
    # ==========================================
    print("Testing update_member()...")
    assert update_member("M001", name="Alice J.") == True
    assert members[0]["name"] == "Alice J."
    assert update_member("M001", email="invalid-email") == False
    print("Member update tests passed.")

    # ==========================================
    # 6. Test Borrowing Books
    # ==========================================
    print("Testing borrow_book()...")
    assert borrow_book("B001", "M001") == True
    assert borrow_book("B001", "M001") == False  # cannot borrow same book twice
    assert borrow_book("B999", "M001") == False  # invalid book
    assert borrow_book("B002", "M999") == False  # invalid member
    print("Borrow tests passed.")

    # ==========================================
    # 7. Test Returning Books
    # ==========================================
    print("Testing return_book()...")
    assert return_book("B001", "M001") == True
    assert return_book("B001", "M001") == False  # cannot return twice
    assert return_book("B999", "M001") == False
    print("Return tests passed.")

    # ==========================================
    # 8. Test Deleting Members and Books
    # ==========================================
    print("Testing delete_member() and delete_book()...")
    assert delete_member("M001") == True
    assert delete_member("M999") == False
    assert delete_book("B001") == True
    assert delete_book("B001") == False
    print("Deletion tests passed.")

    # ==========================================
    # Final Summary
    # ==========================================
    print("\nAll tests completed successfully.")
    print("The system is working as expected.")


if __name__ == "__main__":
    print("Running ReadEasy System Tests...\n")
    run_all_tests()
