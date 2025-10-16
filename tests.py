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
# Automated Testing Module
#
# GitHub: JoshuaYaffa/SmartLibrary-Group-I
# ================================================

"""
This file contains automated test cases for my Mini Library Management System.
The purpose of this file is to test all the main functions in operations.py
and some essential checks from security.py to ensure that the system
works correctly and consistently.
"""

import unittest
import operations
import security


# ==============================================
# Test Class for Library Operations
# ==============================================

class TestLibraryOperations(unittest.TestCase):
    """This class tests all the key features of the library system."""

    def setUp(self):
        """This method runs before each test to reset sample data."""
        self.books = operations.books
        self.members = operations.members

    # ------------------------------
    # Test Book Management Functions
    # ------------------------------

    def test_add_book(self):
        """Test adding a new book."""
        result = operations.add_book("9999999999999", "Test Book", "Test Author", "Testing", 5)
        self.assertTrue(result)
        self.assertIn("9999999999999", self.books)

    def test_update_book(self):
        """Test updating a book record."""
        operations.add_book("8888888888888", "Old Title", "Author", "Genre", 2)
        result = operations.update_book("8888888888888", title="New Title", total_copies=4)
        self.assertTrue(result)
        self.assertEqual(self.books["8888888888888"]["title"], "New Title")
        self.assertEqual(self.books["8888888888888"]["total_copies"], 4)

    def test_delete_book(self):
        """Test deleting a book from the system."""
        operations.add_book("7777777777777", "Delete Me", "Someone", "Drama", 3)
        result = operations.delete_book("7777777777777")
        self.assertTrue(result)
        self.assertNotIn("7777777777777", self.books)

    # ------------------------------
    # Test Member Management
    # ------------------------------

    def test_add_member(self):
        """Test adding a new library member."""
        result = operations.add_member("M999", "Test User", "test@example.com")
        self.assertTrue(result)
        self.assertIn("M999", self.members)

    def test_update_member(self):
        """Test updating a member's details."""
        operations.add_member("M888", "Old Name", "old@example.com")
        result = operations.update_member("M888", name="New Name", email="new@example.com")
        self.assertTrue(result)
        self.assertEqual(self.members["M888"]["name"], "New Name")

    def test_delete_member(self):
        """Test deleting a member record."""
        operations.add_member("M777", "Delete User", "delete@example.com")
        result = operations.delete_member("M777")
        self.assertTrue(result)
        self.assertNotIn("M777", self.members)

    # ------------------------------
    # Test Borrow and Return
    # ------------------------------

    def test_borrow_and_return_book(self):
        """Test borrowing and returning a book."""
        isbn = "91"  # Preloaded Harry Potter book
        member_id = "M001"       # Preloaded member
        result_borrow = operations.borrow_book(isbn, member_id)
        self.assertTrue(result_borrow)
        self.assertIn(isbn, operations.members[member_id]["borrowed_books"])

        result_return = operations.return_book(isbn, member_id)
        self.assertTrue(result_return)
        self.assertNotIn(isbn, operations.members[member_id]["borrowed_books"])

    # ------------------------------
    # Test Preloaded Data
    # ------------------------------

    def test_preloaded_books_exist(self):
        """Check if the 10 preloaded books exist in the system."""
        self.assertGreaterEqual(len(self.books), 10)

    def test_preloaded_members_exist(self):
        """Check if the 10 preloaded members exist in the system."""
        self.assertGreaterEqual(len(self.members), 10)

    # ------------------------------
    # Test Summary Output
    # ------------------------------

    def test_system_summary(self):
        """Ensure the system summary runs without error."""
        try:
            operations.system_summary()
        except Exception as e:
            self.fail(f"System summary raised an exception: {e}")


# ==============================================
# Test Class for Security Features
# ==============================================

class TestSecurityModule(unittest.TestCase):
    """Basic checks for authentication and audit logging."""

    def test_user_roles_exist(self):
        """Ensure default users and roles exist."""
        users = security.USERS
        self.assertIn("admin", users)
        self.assertIn("staff", users)
        self.assertEqual(users["admin"]["role"], "admin")
        self.assertEqual(users["staff"]["role"], "staff")

    def test_log_event_function(self):
        """Test audit log function works properly."""
        try:
            security.log_event("test_user", "performed test action")
        except Exception as e:
            self.fail(f"log_event() raised an exception: {e}")

    def test_log_error_function(self):
        """Test error logging function works properly."""
        try:
            security.log_error("Sample error for testing")
        except Exception as e:
            self.fail(f"log_error() raised an exception: {e}")


# ==============================================
# Run All Tests
# ==============================================

if __name__ == "__main__":
    print("=====================================")
    print(" Running Automated Tests for ReadEasy ")
    print("=====================================\n")
    unittest.main(verbosity=2)
