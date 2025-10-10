"""
ReadEasy Mini Library Management System
Demonstration Script

PROG211 - Individual Assignment
Student: Joshua Yaffa
GitHub: JoshuaYaffa/SmartLibrary-Group-I

This script demonstrates all library system functionality in a realistic scenario.
"""

from operations import *

def demonstrate_library_system():
    """
    Comprehensive demonstration of the ReadEasy Library Management System.
    This shows all CRUD operations and borrow/return functionality in action.
    """
    print("=" * 70)
    print("        READ-EASY LIBRARY MANAGEMENT SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Clear any existing data for a clean demonstration
    books.clear()
    members.clear()
    
    # Step 1: Initialize the system
    print("\n" + "=" * 50)
    print("STEP 1: SYSTEM INITIALIZATION")
    print("=" * 50)
    print("Initializing library system with available genres...")
    print(f"Available genres: {', '.join(GENRES)}")
    
    # Step 2: Add books to the library
    print("\n" + "=" * 50)
    print("STEP 2: ADDING BOOKS TO LIBRARY")
    print("=" * 50)
    
    book_data = [
        ("978-013485", "Python Crash Course", "Eric Matthes", "Non-Fiction", 4),
        ("978-006112", "To Kill a Mockingbird", "Harper Lee", "Fiction", 3),
        ("978-044117", "Dune", "Frank Herbert", "Sci-Fi", 2),
        ("978-014043", "Sherlock Holmes Collection", "Arthur Conan Doyle", "Mystery", 5),
        ("978-145164", "Steve Jobs Biography", "Walter Isaacson", "Biography", 3),
        ("978-043902", "The Hunger Games", "Suzanne Collins", "Fiction", 4),
        ("978-014118", "1984", "George Orwell", "Fiction", 3)
    ]
    
    books_added = 0
    for isbn, title, author, genre, copies in book_data:
        if add_book(isbn, title, author, genre, copies):
            print(f"Added: '{title}' by {author}")
            books_added += 1
        else:
            print(f"Failed to add: '{title}'")
    
    print(f"\nTotal books added: {books_added}")
    
    # Step 3: Register library members
    print("\n" + "=" * 50)
    print("STEP 3: REGISTERING LIBRARY MEMBERS")
    print("=" * 50)
    
    member_data = [
        ("M001", "Alice Johnson", "alice.johnson@email.com"),
        ("M002", "Bob Wilson", "bob.wilson@email.com"),
        ("M003", "Carol Davis", "carol.davis@email.com"),
        ("M004", "David Brown", "david.brown@email.com")
    ]
    
    members_added = 0
    for member_id, name, email in member_data:
        if add_member(member_id, name, email):
            print(f"Registered: {name} ({member_id})")
            members_added += 1
        else:
            print(f"Failed to register: {name}")
    
    print(f"\nTotal members registered: {members_added}")
    
    # Display initial system state
    print("\n" + "=" * 50)
    print("INITIAL SYSTEM STATE")
    print("=" * 50)
    display_system_summary()
    
    # Step 4: Demonstrate search functionality
    print("\n" + "=" * 50)
    print("STEP 4: DEMONSTRATING SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    # Search by title
    print("\nSearching for books with 'Python' in title:")
    python_books = search_books("python", by="title")
    display_search_results(python_books, "title", "python")
    
    # Search by author
    print("\nSearching for books by authors with 'Lee':")
    lee_books = search_books("lee", by="author")
    display_search_results(lee_books, "author", "lee")
    
    # Search with no results
    print("\nSearching for non-existent book:")
    no_books = search_books("nonexistent", by="title")
    display_search_results(no_books, "title", "nonexistent")
    
    # Step 5: Demonstrate book borrowing
    print("\n" + "=" * 50)
    print("STEP 5: DEMONSTRATING BOOK BORROWING")
    print("=" * 50)
    
    print("\nAlice (M001) borrowing books:")
    print(f"- Borrow 'Python Crash Course': {borrow_book('978-013485', 'M001')}")
    print(f"- Borrow 'Dune': {borrow_book('978-044117', 'M001')}")
    print(f"- Borrow '1984': {borrow_book('978-014118', 'M001')}")
    
    print("\nBob (M002) borrowing books:")
    print(f"- Borrow 'The Hunger Games': {borrow_book('978-043902', 'M002')}")
    
    print("\nCarol (M003) attempting to borrow unavailable book:")
    print(f"- Borrow 'Dune' (no copies left): {borrow_book('978-044117', 'M003')}")
    
    # Display borrowed books
    print("\nCurrent borrowed books status:")
    display_borrowed_books('M001')
    display_borrowed_books('M002')
    
    # Step 6: Demonstrate borrowing limits
    print("\n" + "=" * 50)
    print("STEP 6: DEMONSTRATING BORROWING LIMITS")
    print("=" * 50)
    
    print("\nAlice (M001) attempting to borrow fourth book (limit reached):")
    print(f"- Borrow 'Sherlock Holmes': {borrow_book('978-014043', 'M001')}")
    
    # Step 7: Demonstrate book returns
    print("\n" + "=" * 50)
    print("STEP 7: DEMONSTRATING BOOK RETURNS")
    print("=" * 50)
    
    print("\nAlice (M001) returning books:")
    print(f"- Return 'Python Crash Course': {return_book('978-013485', 'M001')}")
    print(f"- Return 'Dune': {return_book('978-044117', 'M001')}")
    
    print("\nAttempting invalid return:")
    print(f"- Return book not borrowed: {return_book('978-043902', 'M001')}")
    
    # Display updated borrowed status
    print("\nUpdated borrowed books status:")
    display_borrowed_books('M001')
    
    # Step 8: Demonstrate update operations
    print("\n" + "=" * 50)
    print("STEP 8: DEMONSTRATING UPDATE OPERATIONS")
    print("=" * 50)
    
    print("\nUpdating book information:")
    print(f"- Update 'Python Crash Course' title: {update_book('978-013485', title='Python Crash Course - Updated Edition')}")
    print(f"- Update copies of '1984': {update_book('978-014118', total_copies=5)}")
    
    print("\nUpdating member information:")
    print(f"- Update Alice's email: {update_member('M001', email='alice.newemail@email.com')}")
    print(f"- Update Bob's name: {update_member('M002', name='Robert Wilson')}")
    
    # Step 9: Demonstrate delete operations
    print("\n" + "=" * 50)
    print("STEP 9: DEMONSTRATING DELETE OPERATIONS")
    print("=" * 50)
    
    print("\nAttempting to delete member with borrowed books:")
    print(f"- Delete Bob (has borrowed books): {delete_member('M002')}")
    
    print("\nBob returning his book:")
    print(f"- Return 'The Hunger Games': {return_book('978-043902', 'M002')}")
    
    print("\nNow attempting to delete Bob:")
    print(f"- Delete Bob (no borrowed books): {delete_member('M002')}")
    
    print("\nAttempting to delete non-existent book:")
    print(f"- Delete invalid ISBN: {delete_book('000-000000')}")
    
    # Step 10: Final system state and summary
    print("\n" + "=" * 50)
    print("FINAL SYSTEM STATE AND SUMMARY")
    print("=" * 50)
    
    display_system_summary()
    display_all_books()
    display_all_members()
    
    # Demonstration summary
    print("\n" + "=" * 70)
    print("DEMONSTRATION SUMMARY")
    print("=" * 70)
    print("Successfully demonstrated:")
    print("- System initialization and genre setup")
    print("- Book and member registration")
    print("- Search functionality (title and author)")
    print("- Book borrowing with availability checks")
    print("- Borrowing limit enforcement (3 books max)")
    print("- Book returns with validation")
    print("- Update operations for books and members")
    print("- Delete operations with safety checks")
    print("- Data integrity throughout all operations")
    print("- Comprehensive error handling")
    print("\nThe ReadEasy Library Management System is fully functional!")
    print("=" * 70)

def interactive_demo():
    """
    Interactive demonstration allowing user input.
    This provides a more engaging experience.
    """
    print("\n" + "=" * 70)
    print("        INTERACTIVE DEMONSTRATION")
    print("=" * 70)
    print("This section allows you to try some library operations.")
    
    # Clear data for interactive demo
    books.clear()
    members.clear()
    
    # Setup some sample data
    add_book("1001", "Interactive Demo Book", "Demo Author", "Fiction", 3)
    add_member("ID001", "Demo User", "demo@email.com")
    
    while True:
        print("\nInteractive Menu:")
        print("1. Search for books")
        print("2. Display all books")
        print("3. Display all members")
        print("4. Show system summary")
        print("5. Exit interactive demo")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            query = input("Enter search term: ").strip()
            search_type = input("Search by (title/author) [title]: ").strip() or "title"
            results = search_books(query, by=search_type)
            display_search_results(results, search_type, query)
            
        elif choice == "2":
            display_all_books()
            
        elif choice == "3":
            display_all_members()
            
        elif choice == "4":
            display_system_summary()
            
        elif choice == "5":
            print("Exiting interactive demo...")
            break
            
        else:
            print("Invalid choice. Please enter 1-5.")

# Main execution
if __name__ == "__main__":
    # Run the comprehensive demonstration
    demonstrate_library_system()
    
    # Optionally run interactive demo
    run_interactive = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
    if run_interactive == 'y':
        interactive_demo()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("Thank you for exploring the ReadEasy Library Management System!")
    print("=" * 70) 
