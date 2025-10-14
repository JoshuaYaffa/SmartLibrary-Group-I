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
# Main Program - Menu and User Interaction
#
# GitHub: JoshuaYaffa/SmartLibrary-Group-I
# ================================================

"""
This is the main program file that runs my Mini Library Management System.
It connects all the functions from operations.py and security.py to create
a working system that supports authentication, user roles, and full CRUD operations.
"""

import security
from operations import (
    add_book, search_books, update_book, delete_book,
    add_member, update_member, delete_member,
    borrow_book, return_book,
    pretty_print_books, pretty_print_members, system_summary
)


# ==============================
# Menu Functions
# ==============================

def admin_menu():
    """
    Displays all available actions for an admin user.
    Admins have full access to manage books, members, and system logs.
    """
    while True:
        print("\n=== ADMIN MENU ===")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. Add Member")
        print("5. Update Member")
        print("6. Delete Member")
        print("7. View All Books")
        print("8. View All Members")
        print("9. Borrow Book")
        print("10. Return Book")
        print("11. System Summary")
        print("12. View Audit Log")
        print("13. View Error Log")
        print("0. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            isbn = input("Enter ISBN: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            genre = input("Enter Genre: ")
            try:
                total_copies = int(input("Enter total copies: "))
            except ValueError:
                print("Invalid input. Total copies must be a number.")
                continue
            if add_book(isbn, title, author, genre, total_copies):
                print("Book added successfully.")
            else:
                print("Failed to add book. Check inputs or duplicates.")

        elif choice == "2":
            isbn = input("Enter ISBN of book to update: ")
            title = input("New Title (leave blank to skip): ") or None
            author = input("New Author (leave blank to skip): ") or None
            genre = input("New Genre (leave blank to skip): ") or None
            total_copies = input("New Total Copies (leave blank to skip): ")
            total_copies = int(total_copies) if total_copies else None
            if update_book(isbn, title, author, genre, total_copies):
                print("Book updated successfully.")
            else:
                print("Failed to update book. Please check ISBN or inputs.")

        elif choice == "3":
            isbn = input("Enter ISBN of book to delete: ")
            if delete_book(isbn):
                print("Book deleted successfully.")
            else:
                print("Failed to delete book. It might be borrowed or not exist.")

        elif choice == "4":
            member_id = input("Enter Member ID: ")
            name = input("Enter Member Name: ")
            email = input("Enter Member Email: ")
            if add_member(member_id, name, email):
                print("Member added successfully.")
            else:
                print("Failed to add member. Check ID or email format.")

        elif choice == "5":
            member_id = input("Enter Member ID to update: ")
            name = input("New Name (leave blank to skip): ") or None
            email = input("New Email (leave blank to skip): ") or None
            if update_member(member_id, name, email):
                print("Member updated successfully.")
            else:
                print("Failed to update member. Please check inputs.")

        elif choice == "6":
            member_id = input("Enter Member ID to delete: ")
            if delete_member(member_id):
                print("Member deleted successfully.")
            else:
                print("Failed to delete member. They might have borrowed books or not exist.")

        elif choice == "7":
            pretty_print_books()

        elif choice == "8":
            pretty_print_members()

        elif choice == "9":
            isbn = input("Enter ISBN: ")
            member_id = input("Enter Member ID: ")
            if borrow_book(isbn, member_id):
                print("Book borrowed successfully.")
            else:
                print("Borrowing failed. Check book or member details.")

        elif choice == "10":
            isbn = input("Enter ISBN: ")
            member_id = input("Enter Member ID: ")
            if return_book(isbn, member_id):
                print("Book returned successfully.")
            else:
                print("Return failed. Verify ISBN and member.")

        elif choice == "11":
            system_summary()

        elif choice == "12":
            security.view_audit_log()

        elif choice == "13":
            security.view_error_log()

        elif choice == "0":
            security.logout()
            break

        else:
            print("Invalid choice. Try again.")


def staff_menu():
    """
    Displays available actions for staff users.
    Staff can manage borrowing and returning but cannot view or delete logs.
    """
    while True:
        print("\n=== STAFF MENU ===")
        print("1. View All Books")
        print("2. View All Members")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. System Summary")
        print("0. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            pretty_print_books()

        elif choice == "2":
            pretty_print_members()

        elif choice == "3":
            isbn = input("Enter ISBN: ")
            member_id = input("Enter Member ID: ")
            if borrow_book(isbn, member_id):
                print("Book borrowed successfully.")
            else:
                print("Borrowing failed. Check book or member details.")

        elif choice == "4":
            isbn = input("Enter ISBN: ")
            member_id = input("Enter Member ID: ")
            if return_book(isbn, member_id):
                print("Book returned successfully.")
            else:
                print("Return failed. Verify ISBN and member.")

        elif choice == "5":
            system_summary()

        elif choice == "0":
            security.logout()
            break

        else:
            print("Invalid choice. Try again.")


# ==============================
# Program Entry Point
# ==============================

def main():
    """
    Main entry point of the system.
    It first authenticates a user and then shows the menu based on their role.
    """
    print("=====================================")
    print(" Welcome to ReadEasy Library System ")
    print("=====================================")

    if not security.authenticate():
        return

    if security.current_user["role"] == "admin":
        admin_menu()
    elif security.current_user["role"] == "staff":
        staff_menu()

    print("\nThank you for using the ReadEasy Mini Library Management System.")


# ==============================
# Program Execution
# ==============================

if __name__ == "__main__":
    main()
