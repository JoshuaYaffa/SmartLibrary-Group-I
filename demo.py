"""
ReadEasy Mini Library Management System
Enhanced Demonstration Script

PROG211 - Individual Assignment
Student: Joshua Mohamed Katibi Yaffa
Class : BSEM1101 Semester 3
ID : 905004075
ID: 905004075
Class : BSEM1101
Semseter: 3
Year : 2

GitHub: JoshuaYaffa/SmartLibrary-Group-I

This script demonstrates all enhanced library system functionality including security features.
"""

from operations import *

def demonstrate_security_features():
    """Demonstrate the comprehensive security system"""
    print("=" * 80)
    print("        SECURITY FEATURES DEMONSTRATION")
    print("=" * 80)
    
    # Clear any existing sessions
    logout()
    
    print("\n1. DEMONSTRATING AUTHENTICATION SYSTEM")
    print("-" * 50)
    
    print("\nTesting failed login attempt:")
    login("hacker", "wrongpassword")
    
    print("\nTesting member login:")
    login("alice", "pass123")
    print(f"Current user: {get_current_user()}")
    logout()
    
    print("\nTesting librarian login:")
    login("librarian1", "lib123")
    print(f"Current user: {get_current_user()}")
    logout()
    
    print("\nTesting admin login:")
    login("admin", "admin123")
    print(f"Current user: {get_current_user()}")
    
    print("\n2. DEMONSTRATING ROLE-BASED ACCESS CONTROL")
    print("-" * 50)
    
    print("\nAdmin permissions demonstration:")
    print("Admin can perform all operations:")
    print(f"  - Add members: {check_permission('add_member')}")
    print(f"  - Delete books: {check_permission('delete_book')}")
    print(f"  - View audit trail: {check_permission('view_audit_trail')}")
    print(f"  - System backup: {check_permission('system_backup')}")
    
    logout()
    
    print("\nLibrarian permissions demonstration:")
    login("librarian1", "lib123")
    print("Librarian can perform library operations:")
    print(f"  - Add books: {check_permission('add_book')}")
    print(f"  - Delete members: {check_permission('delete_member')} (should be False)")
    print(f"  - View system: {check_permission('view_system')}")
    
    logout()
    
    print("\nMember permissions demonstration:")
    login("alice", "pass123")
    print("Member can perform basic operations:")
    print(f"  - Search books: {check_permission('search_books')}")
    print(f"  - Add books: {check_permission('add_book')} (should be False)")
    print(f"  - View own data: {check_permission('view_own_data')}")
    
    logout()

def demonstrate_audit_trail():
    """Demonstrate the comprehensive audit trail system"""
    print("\n" + "=" * 80)
    print("        AUDIT TRAIL DEMONSTRATION")
    print("=" * 80)
    
    # Clear existing data for clean demo
    books.clear()
    members.clear()
    audit_trail["admins"].clear()
    audit_trail["librarians"].clear()
    audit_trail["members"].clear()
    
    print("\n1. GENERATING AUDIT EVENTS")
    print("-" * 50)
    
    print("\nMember activities:")
    login("alice", "pass123")
    search_books("python")
    logout()
    
    print("\nLibrarian activities:")
    login("librarian1", "lib123")
    add_book("1001", "Library Book", "Library Author", "Fiction", 5)
    logout()
    
    print("\nAdmin activities:")
    login("admin", "admin123")
    add_member("DEMO001", "Demo User", "demo@email.com", "123-456-7890")
    system_health_check()
    
    print("\n2. VIEWING AUDIT TRAIL BY ROLE")
    print("-" * 50)
    
    print("\nMember Activities:")
    display_audit_trail("members")
    
    print("\nLibrarian Activities:")
    display_audit_trail("librarians")
    
    print("\nAdmin Activities:")
    display_audit_trail("admins")
    
    print("\n3. SECURITY REPORT")
    print("-" * 50)
    generate_security_report()
    
    print("\n4. INDIVIDUAL USER ACTIVITY")
    print("-" * 50)
    
    print("\nAlice viewing her activity:")
    login("alice", "pass123")
    display_my_activity()
    logout()

def demonstrate_advanced_features():
    """Demonstrate advanced system features"""
    print("\n" + "=" * 80)
    print("        ADVANCED FEATURES DEMONSTRATION")
    print("=" * 80)
    
    login("admin", "admin123")
    
    print("\n1. BATCH OPERATIONS")
    print("-" * 50)
    
    book_list = [
        ("BATCH001", "Batch Book One", "Batch Author", "Fiction", 3),
        ("BATCH002", "Batch Book Two", "Batch Author", "Non-Fiction", 2),
        ("BATCH003", "Batch Book Three", "Batch Author", "Sci-Fi", 4)
    ]
    
    print("Adding multiple books in batch:")
    success_count = batch_add_books(book_list)
    print(f"Batch operation result: {success_count}/{len(book_list)} books added")
    
    print("\n2. SYSTEM HEALTH CHECK")
    print("-" * 50)
    system_health_check()
    
    print("\n3. DATA BACKUP")
    print("-" * 50)
    backup_file = create_backup()
    if backup_file:
        print(f"Backup created: {backup_file}")
    
    print("\n4. DATA EXPORT")
    print("-" * 50)
    export_file = export_books_to_csv()
    if export_file:
        print(f"Data exported: {export_file}")
    
    print("\n5. PERSISTENT STORAGE")
    print("-" * 50)
    print("Data automatically saved throughout operations")
    print(f"Current book count: {len(books)}")
    print(f"Current member count: {len(members)}")
    
    logout()

def demonstrate_library_operations():
    """Demonstrate core library operations with security"""
    print("\n" + "=" * 80)
    print("        LIBRARY OPERATIONS DEMONSTRATION")
    print("=" * 80)
    
    # Clear data for clean demonstration
    books.clear()
    members.clear()
    
    login("admin", "admin123")
    
    print("\n1. SYSTEM INITIALIZATION")
    print("-" * 50)
    print("Initializing library system...")
    print(f"Available genres: {', '.join(GENRES)}")
    
    print("\n2. ADDING BOOKS WITH VALIDATION")
    print("-" * 50)
    
    # Test books with various scenarios
    test_books = [
        ("978-013485", "Python Crash Course", "Eric Matthes", "Non-Fiction", 4),
        ("978-006112", "To Kill a Mockingbird", "Harper Lee", "Fiction", 3),
        ("978-044117", "Dune", "Frank Herbert", "Sci-Fi", 2),
        ("978-014043", "Sherlock Holmes", "Arthur Conan Doyle", "Mystery", 5),
        ("INVALID123", "Invalid Book", "Test Author", "Romance", 1)  # Should fail
    ]
    
    for isbn, title, author, genre, copies in test_books:
        result = add_book(isbn, title, author, genre, copies)
        print(f"Add '{title}': {'SUCCESS' if result else 'FAILED'}")
    
    print("\n3. MEMBER REGISTRATION WITH VALIDATION")
    print("-" * 50)
    
    test_members = [
        ("M001", "Alice Johnson", "alice.johnson@email.com", "123-456-7890"),
        ("M002", "Bob Wilson", "bob.wilson@email.com", "234-567-8901"),
        ("M003", "Carol Davis", "invalid-email", "1234567890"),  # Should fail
        ("M004", "David Brown", "david.brown@email.com", "")
    ]
    
    for member_id, name, email, phone in test_members:
        result = add_member(member_id, name, email, phone)
        print(f"Register {name}: {'SUCCESS' if result else 'FAILED'}")
    
    print("\n4. SEARCH FUNCTIONALITY")
    print("-" * 50)
    
    print("Searching for books with 'Python':")
    results = search_books("python", by="title")
    display_search_results(results, "title", "python")
    
    print("Searching for books by 'Lee':")
    results = search_books("lee", by="author")
    display_search_results(results, "author", "lee")
    
    print("\n5. BORROWING OPERATIONS")
    print("-" * 50)
    
    # Switch to librarian for borrowing operations
    logout()
    login("librarian1", "lib123")
    
    print("Alice borrowing books:")
    print(f"  - Borrow Python Crash Course: {borrow_book('978-013485', 'M001')}")
    print(f"  - Borrow Dune: {borrow_book('978-044117', 'M001')}")
    print(f"  - Borrow Sherlock Holmes: {borrow_book('978-014043', 'M001')}")
    
    print("\nBob borrowing books:")
    print(f"  - Borrow To Kill a Mockingbird: {borrow_book('978-006112', 'M002')}")
    
    print("\nTesting borrowing limits:")
    print(f"  - Alice borrowing fourth book: {borrow_book('978-006112', 'M001')}")
    
    print("\n6. RETURN OPERATIONS")
    print("-" * 50)
    
    print("Alice returning books:")
    print(f"  - Return Python Crash Course: {return_book('978-013485', 'M001')}")
    print(f"  - Return Dune: {return_book('978-044117', 'M001')}")
    
    print("\n7. UPDATE OPERATIONS")
    print("-" * 50)
    
    login("admin", "admin123")
    
    print("Updating book information:")
    print(f"  - Update Python book title: {update_book('978-013485', title='Python Crash Course - Updated Edition')}")
    print(f"  - Update book copies: {update_book('978-044117', total_copies=5)}")
    
    print("Updating member information:")
    print(f"  - Update Alice's email: {update_member('M001', email='alice.new@email.com')}")
    
    print("\n8. SYSTEM OVERVIEW")
    print("-" * 50)
    display_system_summary()
    
    print("\n9. BORROWED BOOKS STATUS")
    print("-" * 50)
    display_borrowed_books('M001')
    display_borrowed_books('M002')
    
    logout()

def demonstrate_persistence():
    """Demonstrate data persistence features"""
    print("\n" + "=" * 80)
    print("        DATA PERSISTENCE DEMONSTRATION")
    print("=" * 80)
    
    login("admin", "admin123")
    
    print("\n1. MANUAL DATA SAVE")
    print("-" * 50)
    save_result = save_data()
    print(f"Manual save: {'SUCCESS' if save_result else 'FAILED'}")
    
    print("\n2. AUTOMATED NOTIFICATIONS")
    print("-" * 50)
    notification_count = send_overdue_notifications()
    print(f"Notifications sent: {notification_count}")
    
    print("\n3. PASSWORD MANAGEMENT")
    print("-" * 50)
    
    # Switch to member for password change test
    logout()
    login("alice", "pass123")
    
    print("Testing password change:")
    print(f"  - Change with wrong current password: {change_password('wrong', 'newpass')}")
    print(f"  - Change with correct password: {change_password('pass123', 'newpass123')}")
    
    # Change back for future demos
    change_password('newpass123', 'pass123')
    
    logout()

def interactive_demo():
    """Interactive demonstration allowing user exploration"""
    print("\n" + "=" * 80)
    print("        INTERACTIVE DEMONSTRATION")
    print("=" * 80)
    print("Explore the library system interactively.")
    print("You can try different operations based on your role.")
    
    while True:
        print("\nINTERACTIVE MENU:")
        print("1. Login to system")
        print("2. View current user")
        print("3. Search books")
        print("4. View all books")
        print("5. View all members")
        print("6. View system summary")
        print("7. View my activity")
        print("8. Logout")
        print("9. Exit interactive demo")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            login(username, password)
            
        elif choice == "2":
            user = get_current_user()
            if user:
                print(f"Current user: {user['username']} ({user['role']})")
                print(f"Full name: {user['full_name']}")
                print(f"Member ID: {user['member_id']}")
            else:
                print("No user logged in")
                
        elif choice == "3":
            if not get_current_user():
                print("Please log in first")
                continue
                
            query = input("Enter search term: ").strip()
            search_type = input("Search by (title/author) [title]: ").strip() or "title"
            results = search_books(query, by=search_type)
            display_search_results(results, search_type, query)
            
        elif choice == "4":
            display_all_books()
            
        elif choice == "5":
            display_all_members()
            
        elif choice == "6":
            display_system_summary()
            
        elif choice == "7":
            display_my_activity()
            
        elif choice == "8":
            logout()
            
        elif choice == "9":
            print("Exiting interactive demo...")
            break
            
        else:
            print("Invalid choice. Please enter 1-9.")

def run_comprehensive_demo():
    """Run the complete demonstration"""
    print("=" * 80)
    print("    READ-EASY LIBRARY MANAGEMENT SYSTEM - COMPREHENSIVE DEMONSTRATION")
    print("=" * 80)
    
    # Ensure clean start
    logout()
    
    try:
        # Run all demonstration sections
        demonstrate_security_features()
        demonstrate_audit_trail()
        demonstrate_advanced_features()
        demonstrate_library_operations()
        demonstrate_persistence()
        
        # Interactive section
        run_interactive = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
        if run_interactive == 'y':
            interactive_demo()
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("FEATURES DEMONSTRATED:")
        print("  SECURITY SYSTEM:")
        print("  - Role-based authentication (Admin, Librarian, Member)")
        print("  - Password hashing and session management")
        print("  - Permission-based access control")
        print("  - Session timeout protection")
        
        print("  AUDIT TRAIL:")
        print("  - Comprehensive activity logging")
        print("  - Role-based event categorization")
        print("  - Timestamp tracking (date, time, month, year)")
        print("  - Security reporting")
        
        print("  ADVANCED FEATURES:")
        print("  - Persistent data storage")
        print("  - System health monitoring")
        print("  - Automated backups")
        print("  - Batch operations")
        print("  - Data export functionality")
        print("  - Enhanced validation")
        
        print("  LIBRARY OPERATIONS:")
        print("  - Complete CRUD operations")
        print("  - Borrow/return with limits")
        print("  - Search functionality")
        print("  - Data integrity maintenance")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"Demonstration error: {e}")
    finally:
        # Ensure clean logout
        logout()

# Main execution
if __name__ == "__main__":
    run_comprehensive_demo()