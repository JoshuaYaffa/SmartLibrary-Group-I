"""
ReadEasy Mini Library Management System
Enhanced Unit Tests

PROG211 - Individual Assignment
Student: Joshua Mohamed Katibi Yaffa
Class : BSEM1101 Semester 3
ID : 905004075
ID: 905004075
Class : BSEM1101
Semseter: 3
Year : 2
GitHub: JoshuaYaffa/SmartLibrary-Group-I

This file contains comprehensive unit tests for all library functions including security features.
"""

# Import all functions from our operations module
from operations import *

def test_add_book():
    """Test the add_book function with various scenarios"""
    print("TESTING add_book() FUNCTION")
    
    # Clear data for clean testing
    books.clear()
    
    # Test 1: Add valid book
    assert add_book("1001", "Python Basics", "John Doe", "Non-Fiction", 5) == True, "Should add valid book"
    
    # Test 2: Add duplicate ISBN
    assert add_book("1001", "Another Book", "Jane Smith", "Fiction", 3) == False, "Should reject duplicate ISBN"
    
    # Test 3: Add book with invalid genre
    assert add_book("1002", "Space Adventure", "Alex Star", "Space Opera", 2) == False, "Should reject invalid genre"
    
    # Test 4: Add book with zero copies
    assert add_book("1003", "Empty Library", "Test Author", "Fiction", 0) == False, "Should reject zero copies"
    
    # Test 5: Verify book was added correctly
    assert "1001" in books, "Book should be in books dictionary"
    assert books["1001"]["title"] == "Python Basics", "Book title should match"
    assert books["1001"]["author"] == "John Doe", "Book author should match"
    
    print("All add_book tests passed!")

def test_add_member():
    """Test the add_member function with various scenarios"""
    print("\nTESTING add_member() FUNCTION")
    
    # Clear data for clean testing
    members.clear()
    
    # Test 1: Add valid member
    assert add_member("M001", "Alice Johnson", "alice@email.com") == True, "Should add valid member"
    
    # Test 2: Add duplicate member ID
    assert add_member("M001", "Bob Wilson", "bob@email.com") == False, "Should reject duplicate member ID"
    
    # Test 3: Verify member was added correctly
    assert len(members) == 1, "Should have one member"
    assert members[0]["member_id"] == "M001", "Member ID should match"
    assert members[0]["borrowed_books"] == [], "Borrowed books should be empty list"
    
    print("All add_member tests passed!")

def test_search_books():
    """Test the search_books function"""
    print("\nTESTING search_books() FUNCTION")
    
    # Clear and setup test data
    books.clear()
    add_book("2001", "Python Programming", "John Smith", "Non-Fiction", 3)
    add_book("2002", "The Great Python", "Jane Doe", "Fiction", 2)
    add_book("2003", "Java Basics", "Bob Johnson", "Non-Fiction", 4)
    
    # Test 1: Search by title (partial match)
    results = search_books("python", by="title")
    assert len(results) == 2, "Should find 2 books with 'python' in title"
    
    # Test 2: Search by author
    results = search_books("smith", by="author")
    assert len(results) == 1, "Should find 1 book by author 'Smith'"
    
    # Test 3: Search with no results
    results = search_books("nonexistent", by="title")
    assert len(results) == 0, "Should find no books for nonexistent term"
    
    # Test 4: Case insensitive search
    results = search_books("PYTHON", by="title")
    assert len(results) == 2, "Should be case insensitive"
    
    print("All search_books tests passed!")

def test_update_functions():
    """Test update_book and update_member functions"""
    print("\nTESTING UPDATE FUNCTIONS")
    
    # Setup test data
    books.clear()
    members.clear()
    add_book("3001", "Original Title", "Original Author", "Fiction", 5)
    add_member("M100", "Original Name", "original@email.com")
    
    # Test 1: Update book title
    assert update_book("3001", title="New Title") == True, "Should update book title"
    assert books["3001"]["title"] == "New Title", "Book title should be updated"
    
    # Test 2: Update book with invalid genre
    assert update_book("3001", genre="Invalid Genre") == False, "Should reject invalid genre"
    
    # Test 3: Update non-existent book
    assert update_book("9999", title="No Book") == False, "Should fail for non-existent book"
    
    # Test 4: Update member name
    assert update_member("M100", name="New Name") == True, "Should update member name"
    
    # Test 5: Update non-existent member
    assert update_member("M999", name="No One") == False, "Should fail for non-existent member"
    
    print("All update function tests passed!")

def test_delete_functions():
    """Test delete_book and delete_member functions"""
    print("\nTESTING DELETE FUNCTIONS")
    
    # Setup test data
    books.clear()
    members.clear()
    add_book("4001", "Book to Delete", "Author", "Fiction", 3)
    add_member("M200", "Member to Delete", "delete@email.com")
    
    # Test 1: Delete existing book
    assert delete_book("4001") == True, "Should delete existing book"
    assert "4001" not in books, "Book should be removed from dictionary"
    
    # Test 2: Delete non-existent book
    assert delete_book("9999") == False, "Should fail for non-existent book"
    
    # Test 3: Delete existing member
    assert delete_member("M200") == True, "Should delete existing member"
    assert len(members) == 0, "Member should be removed from list"
    
    # Test 4: Delete non-existent member
    assert delete_member("M999") == False, "Should fail for non-existent member"
    
    print("All delete function tests passed!")

def test_borrow_return_functions():
    """Test borrow_book and return_book functions"""
    print("\nTESTING BORROW AND RETURN FUNCTIONS")
    
    # Setup test data
    books.clear()
    members.clear()
    add_book("5001", "Borrowable Book", "Author", "Fiction", 2)
    add_book("5002", "Another Book", "Author", "Non-Fiction", 1)
    add_member("M300", "Borrowing Member", "borrow@email.com")
    
    # Test 1: Successful borrow
    assert borrow_book("5001", "M300") == True, "Should allow borrowing available book"
    assert books["5001"]["total_copies"] == 1, "Should decrease available copies"
    assert "5001" in members[0]["borrowed_books"], "Book should be in member's borrowed list"
    
    # Test 2: Borrow same book again
    assert borrow_book("5001", "M300") == False, "Should not allow borrowing same book twice"
    
    # Test 3: Borrow non-existent book
    assert borrow_book("9999", "M300") == False, "Should not allow borrowing non-existent book"
    
    # Test 4: Borrow with non-existent member
    assert borrow_book("5001", "M999") == False, "Should not allow borrowing with non-existent member"
    
    # Test 5: Successful return
    assert return_book("5001", "M300") == True, "Should allow returning borrowed book"
    assert books["5001"]["total_copies"] == 2, "Should increase available copies"
    assert "5001" not in members[0]["borrowed_books"], "Book should be removed from borrowed list"
    
    # Test 6: Return non-borrowed book
    assert return_book("5002", "M300") == False, "Should not allow returning non-borrowed book"
    
    # Test 7: Test borrowing limit (3 books)
    borrow_book("5001", "M300")
    borrow_book("5002", "M300")
    add_book("5003", "Third Book", "Author", "Sci-Fi", 1)
    assert borrow_book("5003", "M300") == True, "Should allow third book"
    add_book("5004", "Fourth Book", "Author", "Mystery", 1)
    assert borrow_book("5004", "M300") == False, "Should reject fourth book (limit reached)"
    
    print("All borrow/return function tests passed!")

def test_validation_helpers():
    """Test data validation helper functions"""
    print("\nTESTING VALIDATION HELPER FUNCTIONS")
    
    # Setup test data
    books.clear()
    members.clear()
    add_book("6001", "Test Book", "Test Author", "Fiction", 3)
    add_member("M400", "Test Member", "test@email.com")
    
    # Test genre validation
    assert is_valid_genre("Fiction") == True, "Should validate Fiction as valid genre"
    assert is_valid_genre("Romance") == False, "Should reject Romance as invalid genre"
    
    # Test book existence
    assert book_exists("6001") == True, "Should find existing book"
    assert book_exists("9999") == False, "Should not find non-existent book"
    
    # Test member existence
    assert member_exists("M400") == True, "Should find existing member"
    assert member_exists("M999") == False, "Should not find non-existent member"
    
    print("All validation helper tests passed!")

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\nTESTING EDGE CASES")
    
    # Clear all data
    books.clear()
    members.clear()
    
    # Test 1: Delete book that is borrowed
    add_book("7001", "Popular Book", "Author", "Fiction", 1)
    add_member("M500", "Reader", "reader@email.com")
    borrow_book("7001", "M500")
    assert delete_book("7001") == False, "Should not delete borrowed book"
    
    # Test 2: Delete member with borrowed books
    assert delete_member("M500") == False, "Should not delete member with borrowed books"
    
    # Test 3: Borrow when no copies available
    add_book("7002", "Single Copy Book", "Author", "Non-Fiction", 1)
    borrow_book("7002", "M500")
    add_member("M600", "Another Reader", "another@email.com")
    assert borrow_book("7002", "M600") == False, "Should not borrow when no copies available"
    
    # Test 4: Update book with negative copies
    add_book("7003", "Test Book", "Author", "Biography", 5)
    assert update_book("7003", total_copies=-1) == False, "Should reject negative copies"
    
    # Test 5: Return book that was never borrowed
    add_book("7004", "New Book", "Author", "Mystery", 3)
    assert return_book("7004", "M500") == False, "Should not return book that was never borrowed"
    
    print("All edge case tests passed!")

def test_data_integrity():
    """Test data integrity across multiple operations"""
    print("\nTESTING DATA INTEGRITY")
    
    # Clear all data
    books.clear()
    members.clear()
    
    # Setup initial data
    add_book("8001", "Integrity Test Book", "Test Author", "Fiction", 2)
    add_member("M700", "Integrity Test Member", "integrity@email.com")
    
    # Test 1: Borrow and return maintains data consistency
    initial_copies = books["8001"]["total_copies"]
    assert borrow_book("8001", "M700") == True, "Should borrow successfully"
    assert books["8001"]["total_copies"] == initial_copies - 1, "Copies should decrease after borrow"
    assert "8001" in members[0]["borrowed_books"], "Book should be in borrowed list"
    
    assert return_book("8001", "M700") == True, "Should return successfully"
    assert books["8001"]["total_copies"] == initial_copies, "Copies should restore after return"
    assert "8001" not in members[0]["borrowed_books"], "Book should be removed from borrowed list"
    
    # Test 2: Multiple operations maintain state
    add_book("8002", "Second Book", "Second Author", "Non-Fiction", 1)
    add_member("M701", "Second Member", "second@email.com")
    
    borrow_book("8001", "M700")
    borrow_book("8002", "M701")
    
    assert len(members[0]["borrowed_books"]) == 1, "First member should have 1 book"
    assert len(members[1]["borrowed_books"]) == 1, "Second member should have 1 book"
    assert books["8001"]["total_copies"] == 1, "First book should have 1 copy left"
    assert books["8002"]["total_copies"] == 0, "Second book should have 0 copies left"
    
    print("All data integrity tests passed!")

def test_security_system():
    """Test the security and authentication system"""
    print("\nTESTING SECURITY SYSTEM")
    
    # Clear any existing sessions
    logout()
    
    # Test 1: Login with valid credentials
    print("Testing login with valid credentials:")
    assert login("admin", "admin123") == True, "Admin should login successfully"
    assert current_user["role"] == "admin", "Current user should have admin role"
    
    # Test 2: Login with invalid credentials
    print("Testing login with invalid credentials:")
    logout()
    assert login("admin", "wrongpassword") == False, "Should reject wrong password"
    assert current_user is None, "Current user should be None after failed login"
    
    # Test 3: Test permissions
    print("Testing role-based permissions:")
    login("admin", "admin123")
    assert check_permission("add_member") == True, "Admin should have add_member permission"
    assert check_permission("delete_book") == True, "Admin should have delete_book permission"
    
    logout()
    login("librarian1", "lib123")
    assert check_permission("add_book") == True, "Librarian should have add_book permission"
    assert check_permission("delete_member") == False, "Librarian should NOT have delete_member permission"
    
    logout()
    login("alice", "pass123")
    assert check_permission("search_books") == True, "Member should have search_books permission"
    assert check_permission("add_book") == False, "Member should NOT have add_book permission"
    
    logout()
    print("All security tests passed!")

def test_audit_trail():
    """Test the audit trail functionality"""
    print("\nTESTING AUDIT TRAIL FUNCTIONALITY")
    
    # Clear audit trail for testing
    audit_trail["admins"].clear()
    audit_trail["librarians"].clear()
    audit_trail["members"].clear()
    
    # Test 1: Login creates audit entry
    login("admin", "admin123")
    assert len(audit_trail["admins"]) > 0, "Login should create audit entry"
    
    # Test 2: Operations create audit entries
    initial_audit_count = len(audit_trail["admins"])
    add_book("9001", "Audit Test Book", "Test Author", "Fiction", 3)
    assert len(audit_trail["admins"]) > initial_audit_count, "Book addition should create audit entry"
    
    # Test 3: Logout creates audit entry
    initial_audit_count = len(audit_trail["admins"])
    logout()
    assert len(audit_trail["admins"]) > initial_audit_count, "Logout should create audit entry"
    
    # Test 4: Failed login creates audit entry
    initial_audit_count = len(audit_trail["admins"])
    login("hacker", "wrongpassword")
    assert len(audit_trail["admins"]) > initial_audit_count, "Failed login should create audit entry"
    
    print("All audit trail tests passed!")

def test_persistent_storage():
    """Test data persistence functionality"""
    print("\nTESTING PERSISTENT STORAGE")
    
    # Clear data and setup test data
    books.clear()
    members.clear()
    add_book("10001", "Persistent Book", "Storage Author", "Fiction", 5)
    add_member("M900", "Persistent Member", "persistent@email.com")
    
    # Test 1: Save data
    assert save_data() == True, "Should save data successfully"
    
    # Remember current state
    original_book_count = len(books)
    original_member_count = len(members)
    
    # Clear current data
    books.clear()
    members.clear()
    
    # Test 2: Load data
    assert load_data() == True, "Should load data successfully"
    assert len(books) == original_book_count, "Should restore saved books"
    assert len(members) == original_member_count, "Should restore saved members"
    
    print("All persistent storage tests passed!")

def test_advanced_features():
    """Test advanced system features"""
    print("\nTESTING ADVANCED FEATURES")
    
    # Setup for testing
    login("admin", "admin123")
    books.clear()
    members.clear()
    
    # Test 1: Batch operations
    book_list = [
        ("B001", "Batch Book 1", "Batch Author", "Fiction", 2),
        ("B002", "Batch Book 2", "Batch Author", "Non-Fiction", 3),
        ("B003", "Batch Book 3", "Batch Author", "Sci-Fi", 1)
    ]
    
    success_count = batch_add_books(book_list)
    assert success_count == 3, "Should add all books in batch"
    assert len(books) == 3, "Should have 3 books after batch operation"
    
    # Test 2: System health check
    health_ok = system_health_check()
    assert health_ok == True, "System health should be OK with valid data"
    
    # Test 3: Backup creation
    backup_file = create_backup()
    assert backup_file is not None, "Should create backup file"
    assert "backup_library_" in backup_file, "Backup filename should follow pattern"
    
    # Test 4: Data export
    export_file = export_books_to_csv()
    assert export_file is not None, "Should create export file"
    assert "library_books_export_" in export_file, "Export filename should follow pattern"
    
    logout()
    print("All advanced features tests passed!")

def test_validation_functions():
    """Test enhanced validation functions"""
    print("\nTESTING ENHANCED VALIDATION FUNCTIONS")
    
    # Test email validation
    assert validate_email("test@example.com") == True, "Should validate correct email"
    assert validate_email("invalid-email") == False, "Should reject invalid email"
    assert validate_email("a@b.c") == True, "Should validate short but valid email"
    
    # Test ISBN validation
    assert validate_isbn("978-0123456789") == True, "Should validate ISBN with hyphens"
    assert validate_isbn("0123456789") == True, "Should validate 10-digit ISBN"
    assert validate_isbn("9780123456789") == True, "Should validate 13-digit ISBN"
    assert validate_isbn("invalid") == False, "Should reject invalid ISBN"
    
    # Test phone validation
    assert validate_phone("123-456-7890") == True, "Should validate phone with hyphens"
    assert validate_phone("(123) 456-7890") == True, "Should validate phone with parentheses"
    assert validate_phone("1234567890") == True, "Should validate plain phone number"
    assert validate_phone("123") == False, "Should reject too short phone number"
    
    print("All validation function tests passed!")

def run_all_tests():
    """Run all unit tests"""
    print("=" * 70)
    print("RUNNING ALL ENHANCED UNIT TESTS")
    print("=" * 70)
    
    # Ensure we start with no active session
    logout()
    
    # Run all test functions
    test_add_book()
    test_add_member()
    test_search_books()
    test_update_functions()
    test_delete_functions()
    test_borrow_return_functions()
    test_validation_helpers()
    test_edge_cases()
    test_data_integrity()
    test_security_system()
    test_audit_trail()
    test_persistent_storage()
    test_advanced_features()
    test_validation_functions()
    
    # Final cleanup
    logout()
    
    print("\n" + "=" * 70)
    print("ALL ENHANCED UNIT TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)
    print("TEST SUMMARY:")
    print(f"   Total books in system: {len(books)}")
    print(f"   Total members in system: {len(members)}")
    print(f"   Total audit events: {sum(len(v) for v in audit_trail.values())}")
    print("   All CRUD operations verified")
    print("   All security features verified")
    print("   All advanced features verified")
    print("   All validation functions verified")
    print("   Data integrity maintained")
    print("   Persistent storage working")
    print("   Audit trail functioning")
    print("   All assignment requirements satisfied")
    print("=" * 70)

# Run tests when file is executed directly
if __name__ == "__main__":
    run_all_tests()