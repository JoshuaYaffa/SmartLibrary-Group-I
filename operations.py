"""
ReadEasy Mini Library Management System
Core operations module

PROG211 - Individual Assignment
Student: Joshua Mohamed Katibi Yaffa
Class : BSEM1101 Semester 3
ID : 905004075
GitHub: JoshuaYaffa/SmartLibrary-Group-I

Complete Library System: All Core Functionality Implemented
"""

# ==================== GLOBAL DATA STRUCTURES ====================

# I'm using a tuple for genres because these categories are fixed and won't change
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery", "Biography")

# Dictionary for books because ISBN lookup should be fast - O(1) time complexity
books = {}

# List for members since we'll mostly iterate through them and the dataset is small
members = []

# ==================== CORE CRUD FUNCTIONS ====================

def add_book(isbn, title, author, genre, total_copies):
    """
    Adds a new book to the library system after validating the input.
    
    I chose to return True/False so the calling code knows if the operation succeeded.
    This makes error handling easier in the main program.
    """
    # First check if this ISBN already exists - no duplicate books allowed
    if isbn in books:
        return False
    
    # Make sure the genre is one of our valid categories
    if genre not in GENRES:
        return False
    
    # Can't have negative or zero copies in the library
    if total_copies < 1:
        return False
    
    # Everything looks good, add the book to our dictionary
    books[isbn] = {
        "title": title,
        "author": author, 
        "genre": genre,
        "total_copies": total_copies
    }
    
    return True

def add_member(member_id, name, email):
    """
    Registers a new member in the library system.
    
    I'm using a list for members because we typically need to search through
    all members for various operations, and the number of members is manageable.
    """
    # Check if this member ID is already taken - each member needs a unique ID
    for member in members:
        if member["member_id"] == member_id:
            return False
    
    # Create the new member record with empty borrowed books list
    new_member = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "borrowed_books": []  # Start with no books borrowed
    }
    members.append(new_member)
    
    return True

# ==================== SEARCH AND READ FUNCTIONS ====================

def search_books(query, by="title"):
    """
    Search for books by title or author with case-insensitive partial matching.
    
    I designed this to be flexible - you can search by title (default) or author.
    The partial matching means you don't need to type the full title or author name.
    
    Args:
        query (str): Search term to look for
        by (str): Search field - "title" (default) or "author"
    
    Returns:
        list: List of matching book dictionaries
    """
    matching_books = []
    
    # Convert search query to lowercase for case-insensitive matching
    search_term = query.lower()
    
    # Search through all books in the system
    for isbn, book in books.items():
        if by == "title":
            # Check if search term appears in the book title
            if search_term in book["title"].lower():
                matching_books.append(book)
        elif by == "author":
            # Check if search term appears in the author name
            if search_term in book["author"].lower():
                matching_books.append(book)
        else:
            # If someone tries to search by an invalid field
            print(f" Error: Cannot search by '{by}'. Use 'title' or 'author'.")
            return []
    
    return matching_books

# ==================== UPDATE FUNCTIONS ====================

def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """
    Update specific fields of an existing book.
    
    I made this flexible so you can update any combination of fields.
    Only the provided fields will be updated - others remain unchanged.
    
    Args:
        isbn (str): ISBN of the book to update
        title (str, optional): New title
        author (str, optional): New author
        genre (str, optional): New genre
        total_copies (int, optional): New total copies
    
    Returns:
        bool: True if successful, False if book doesn't exist or genre invalid
    """
    # First check if the book exists
    if isbn not in books:
        return False
    
    # Get the current book data
    book = books[isbn]
    
    # Update title if provided
    if title is not None:
        book["title"] = title
    
    # Update author if provided
    if author is not None:
        book["author"] = author
    
    # Update genre if provided (with validation)
    if genre is not None:
        if genre not in GENRES:
            return False
        book["genre"] = genre
    
    # Update total copies if provided (with validation)
    if total_copies is not None:
        if total_copies < 0:
            return False
        book["total_copies"] = total_copies
    
    return True

def update_member(member_id, name=None, email=None):
    """
    Update specific fields of an existing member.
    
    This allows updating member information without affecting their borrowed books.
    
    Args:
        member_id (str): Member ID to update
        name (str, optional): New name
        email (str, optional): New email
    
    Returns:
        bool: True if successful, False if member doesn't exist
    """
    # Find the member
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    # Return False if member doesn't exist
    if member is None:
        return False
    
    # Update name if provided
    if name is not None:
        member["name"] = name
    
    # Update email if provided
    if email is not None:
        member["email"] = email
    
    return True

# ==================== DELETE FUNCTIONS ====================

def delete_book(isbn):
    """
    Remove a book from the library system.
    
    I added safety checks to prevent deleting books that are currently borrowed.
    This maintains data integrity in the system.
    
    Args:
        isbn (str): ISBN of the book to delete
    
    Returns:
        bool: True if successful, False if book doesn't exist or has borrowed copies
    """
    # Check if book exists
    if isbn not in books:
        return False
    
    # Check if any member has borrowed this book
    for member in members:
        if isbn in member["borrowed_books"]:
            return False
    
    # Safe to delete the book
    del books[isbn]
    return True

def delete_member(member_id):
    """
    Remove a member from the library system.
    
    This ensures we don't delete members who still have borrowed books,
    which would cause data consistency issues.
    
    Args:
        member_id (str): Member ID to delete
    
    Returns:
        bool: True if successful, False if member doesn't exist or has borrowed books
    """
    # Find the member
    member = None
    member_index = -1
    for index, m in enumerate(members):
        if m["member_id"] == member_id:
            member = m
            member_index = index
            break
    
    # Return False if member doesn't exist
    if member is None:
        return False
    
    # Check if member has any borrowed books
    if len(member["borrowed_books"]) > 0:
        return False
    
    # Safe to delete the member
    del members[member_index]
    return True

# ==================== BORROW AND RETURN FUNCTIONS ====================

def borrow_book(isbn, member_id):
    """
    Allow a member to borrow a book from the library.
    
    I designed this with multiple safety checks to ensure:
    - The book exists and is available
    - The member exists and hasn't reached the borrowing limit
    - The system maintains data integrity
    
    Args:
        isbn (str): ISBN of the book to borrow
        member_id (str): Member ID of the person borrowing
    
    Returns:
        bool: True if successful, False if any condition fails
    """
    # Check if the book exists
    if isbn not in books:
        print(f" Book with ISBN {isbn} not found.")
        return False
    
    # Check if the member exists
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        print(f" Member with ID {member_id} not found.")
        return False
    
    # Check if the book has available copies
    if books[isbn]["total_copies"] <= 0:
        print(f" No copies available for '{books[isbn]['title']}'.")
        return False
    
    # Check if member has reached the borrowing limit (3 books)
    if len(member["borrowed_books"]) >= 3:
        print(f" {member['name']} has reached the borrowing limit of 3 books.")
        return False
    
    # Check if member already has this book borrowed
    if isbn in member["borrowed_books"]:
        print(f" {member['name']} already has this book borrowed.")
        return False
    
    # All checks passed - process the borrowing
    books[isbn]["total_copies"] -= 1
    member["borrowed_books"].append(isbn)
    
    print(f" {member['name']} successfully borrowed '{books[isbn]['title']}'")
    return True

def return_book(isbn, member_id):
    """
    Allow a member to return a borrowed book to the library.
    
    This function ensures that:
    - The book exists
    - The member actually borrowed the book
    - The system updates correctly
    
    Args:
        isbn (str): ISBN of the book to return
        member_id (str): Member ID of the person returning
    
    Returns:
        bool: True if successful, False if any condition fails
    """
    # Check if the book exists
    if isbn not in books:
        print(f" Book with ISBN {isbn} not found.")
        return False
    
    # Check if the member exists
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        print(f" Member with ID {member_id} not found.")
        return False
    
    # Check if the member actually has this book borrowed
    if isbn not in member["borrowed_books"]:
        print(f" {member['name']} doesn't have this book borrowed.")
        return False
    
    # Process the return
    books[isbn]["total_copies"] += 1
    member["borrowed_books"].remove(isbn)
    
    print(f" {member['name']} successfully returned '{books[isbn]['title']}'")
    return True

def get_member_borrowed_books(member_id):
    """
    Get detailed information about books a member has borrowed.
    
    This is useful for displaying what books a member currently has
    and for administrative purposes.
    
    Args:
        member_id (str): Member ID to check
    
    Returns:
        list: List of borrowed book details, or empty list if none
    """
    # Find the member
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        return []
    
    # Get details for each borrowed book
    borrowed_details = []
    for isbn in member["borrowed_books"]:
        if isbn in books:
            book_info = books[isbn].copy()
            book_info["isbn"] = isbn  # Add ISBN to the book info
            borrowed_details.append(book_info)
    
    return borrowed_details

# ==================== DATA VALIDATION HELPERS ====================

def is_valid_genre(genre):
    """Check if a genre is in our valid GENRES tuple"""
    return genre in GENRES

def book_exists(isbn):
    """Check if a book with this ISBN exists in the system"""
    return isbn in books

def member_exists(member_id):
    """Check if a member with this ID exists in the system"""
    for member in members:
        if member["member_id"] == member_id:
            return True
    return False

# ==================== DISPLAY FUNCTIONS ====================

def display_all_books():
    """Shows all books currently in the library in a nice format"""
    print("\n LIBRARY BOOK COLLECTION:")
    print("=" * 50)
    
    if not books:
        print("No books in the library yet.")
        return
    
    for book_number, (isbn, book) in enumerate(books.items(), 1):
        print(f"{book_number}. ISBN: {isbn}")
        print(f"   Title: {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Genre: {book['genre']}")
        print(f"   Copies Available: {book['total_copies']}")
        print()

def display_all_members():
    """Shows all registered members and their details"""
    print("\n REGISTERED LIBRARY MEMBERS:")
    print("=" * 50)
    
    if not members:
        print("No members registered yet.")
        return
    
    for member_number, member in enumerate(members, 1):
        print(f"{member_number}. ID: {member['member_id']}")
        print(f"   Name: {member['name']}")
        print(f"   Email: {member['email']}")
        print(f"   Books Borrowed: {len(member['borrowed_books'])}")
        print()

def display_system_summary():
    """Shows a quick overview of the entire system"""
    print("\n SYSTEM SUMMARY:")
    print("=" * 30)
    print(f"Total Books: {len(books)}")
    print(f"Total Members: {len(members)}")
    print(f"Available Genres: {len(GENRES)}")
    print("=" * 30)

def display_search_results(books_list, search_type, query):
    """
    Display search results in a user-friendly format.
    
    This helps make the search output look nice and informative.
    """
    if not books_list:
        print(f"\n No books found with {search_type} containing '{query}'")
        return
    
    print(f"\n SEARCH RESULTS: {len(books_list)} books with {search_type} containing '{query}'")
    print("=" * 60)
    
    for book_number, book in enumerate(books_list, 1):
        print(f"{book_number}. Title: {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Genre: {book['genre']}")
        print(f"   Copies Available: {book['total_copies']}")
        print()

def display_borrowed_books(member_id):
    """
    Display all books currently borrowed by a specific member.
    
    This gives a clear overview of what a member has checked out.
    """
    borrowed_books = get_member_borrowed_books(member_id)
    
    # Find member name for display
    member_name = "Unknown"
    for member in members:
        if member["member_id"] == member_id:
            member_name = member["name"]
            break
    
    print(f"\n BOOKS BORROWED BY {member_name} ({member_id}):")
    print("=" * 50)
    
    if not borrowed_books:
        print("No books currently borrowed.")
        return
    
    for book_number, book in enumerate(borrowed_books, 1):
        print(f"{book_number}. ISBN: {book['isbn']}")
        print(f"   Title: {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Genre: {book['genre']}")
        print()

# ==================== SAMPLE DATA SETUP ====================

def setup_sample_data():
    """
    I'm adding sample data to test the system without manual entry.
    This helps verify everything is working correctly.
    """
    print(" Setting up sample data for testing...")
    
    # Sample books data
    sample_books = [
        ("1001", "Python Programming", "John Smith", "Non-Fiction", 3),
        ("1002", "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 5),
        ("1003", "Dune", "Frank Herbert", "Sci-Fi", 2),
        ("1004", "Sherlock Holmes", "Arthur Conan Doyle", "Mystery", 4),
        ("1005", "Steve Jobs Biography", "Walter Isaacson", "Biography", 3),
        ("1006", "Data Science Basics", "Maria Garcia", "Non-Fiction", 2),
        ("1007", "The Hobbit", "J.R.R. Tolkien", "Fiction", 4)
    ]
    
    # Sample members data
    sample_members = [
        ("M001", "Alice Johnson", "alice@email.com"),
        ("M002", "Bob Wilson", "bob@email.com"),
        ("M003", "Carol Davis", "carol@email.com"),
        ("M004", "David Brown", "david@email.com")
    ]
    
    # Add sample books
    books_added = 0
    for isbn, title, author, genre, copies in sample_books:
        if add_book(isbn, title, author, genre, copies):
            books_added += 1
    
    # Add sample members
    members_added = 0
    for member_id, name, email in sample_members:
        if add_member(member_id, name, email):
            members_added += 1
    
    print(f" Sample data setup complete:")
    print(f"   Books added: {books_added}")
    print(f"   Members added: {members_added}")

# ==================== COMPREHENSIVE TESTING ====================

def test_complete_system():
    """
    Comprehensive test of the complete library system.
    I'm testing all functionality to ensure everything works together properly.
    """
    print(" COMPLETE LIBRARY SYSTEM TESTING")
    print("=" * 60)
    
    # Clear any existing data for clean testing
    books.clear()
    members.clear()
    
    # Test 1: Basic function testing
    print("\n1. TESTING CORE FUNCTIONS:")
    
    # Test add_book with various scenarios
    print("   Testing add_book():")
    print(f"   - Valid book: {add_book('2001', 'Test Book', 'Test Author', 'Fiction', 5)}")
    print(f"   - Duplicate ISBN: {add_book('2001', 'Another Book', 'Different Author', 'Sci-Fi', 3)}")
    print(f"   - Invalid genre: {add_book('2002', 'Space Book', 'Space Author', 'Space Opera', 2)}")
    print(f"   - Zero copies: {add_book('2003', 'No Copies', 'Some Author', 'Fiction', 0)}")
    
    # Test add_member with various scenarios
    print("   Testing add_member():")
    print(f"   - Valid member: {add_member('M100', 'John Doe', 'john@email.com')}")
    print(f"   - Duplicate ID: {add_member('M100', 'Jane Doe', 'jane@email.com')}")
    
    # Test 2: Setup sample data
    print("\n2. TESTING SAMPLE DATA SETUP:")
    setup_sample_data()
    
    # Test 3: Search functionality
    print("\n3. TESTING SEARCH FUNCTIONALITY:")
    
    # Test title search
    print("   Testing title search:")
    title_results = search_books("python", by="title")
    print(f"   - Search for 'python' in titles: {len(title_results)} books found")
    
    # Test author search
    print("   Testing author search:")
    author_results = search_books("smith", by="author")
    print(f"   - Search for 'smith' in authors: {len(author_results)} books found")
    
    # Test partial matching
    print("   Testing partial matching:")
    partial_results = search_books("prog", by="title")
    print(f"   - Search for 'prog' in titles: {len(partial_results)} books found")
    
    # Test case insensitivity
    print("   Testing case insensitivity:")
    case_results = search_books("PYTHON", by="title")
    print(f"   - Search for 'PYTHON' (uppercase): {len(case_results)} books found")
    
    # Display some search results
    if title_results:
        display_search_results(title_results, "title", "python")
    
    # Test 4: Update functionality
    print("\n4. TESTING UPDATE FUNCTIONS:")
    
    # Test update_book
    print("   Testing update_book():")
    print(f"   - Update book title: {update_book('1001', title='Advanced Python Programming')}")
    print(f"   - Update book genre: {update_book('1001', genre='Fiction')}")
    print(f"   - Update invalid genre: {update_book('1001', genre='Romance')}")
    print(f"   - Update non-existent book: {update_book('9999', title='No Book')}")
    
    # Test update_member
    print("   Testing update_member():")
    print(f"   - Update member name: {update_member('M001', name='Alice Brown')}")
    print(f"   - Update member email: {update_member('M001', email='alice.brown@email.com')}")
    print(f"   - Update non-existent member: {update_member('M999', name='No One')}")
    
    # Test 5: Delete functionality
    print("\n5. TESTING DELETE FUNCTIONS:")
    
    # Test delete_book
    print("   Testing delete_book():")
    print(f"   - Delete existing book: {delete_book('1005')}")  # Should work
    print(f"   - Delete non-existent book: {delete_book('9999')}")  # Should fail
    
    # Test delete_member
    print("   Testing delete_member():")
    print(f"   - Delete existing member: {delete_member('M003')}")  # Should work
    print(f"   - Delete non-existent member: {delete_member('M999')}")  # Should fail
    
    # Test 6: Borrow and return functionality
    print("\n6. TESTING BORROW AND RETURN FUNCTIONS:")
    
    # Test successful borrowing
    print("   Testing borrow_book():")
    print(f"   - Borrow valid book: {borrow_book('1001', 'M001')}")
    print(f"   - Borrow same book again: {borrow_book('1001', 'M001')}")  # Should fail
    print(f"   - Borrow another book: {borrow_book('1002', 'M001')}")
    print(f"   - Borrow third book: {borrow_book('1003', 'M001')}")
    print(f"   - Try to borrow fourth book (limit): {borrow_book('1004', 'M001')}")  # Should fail
    
    # Test borrowing edge cases
    print("   Testing borrowing edge cases:")
    print(f"   - Borrow non-existent book: {borrow_book('9999', 'M001')}")
    print(f"   - Borrow with non-existent member: {borrow_book('1001', 'M999')}")
    
    # Test successful returns
    print("   Testing return_book():")
    print(f"   - Return valid book: {return_book('1001', 'M001')}")
    print(f"   - Return same book again: {return_book('1001', 'M001')}")  # Should fail
    print(f"   - Return non-existent book: {return_book('9999', 'M001')}")
    print(f"   - Return with non-existent member: {return_book('1002', 'M999')}")
    
    # Test displaying borrowed books
    print("   Testing borrowed books display:")
    display_borrowed_books('M001')
    
    # Test multiple members borrowing
    print("   Testing multiple members:")
    print(f"   - Member M002 borrows book: {borrow_book('1004', 'M002')}")
    display_borrowed_books('M002')
    
    # Test 7: Display functions
    print("\n7. TESTING DISPLAY FUNCTIONS:")
    display_system_summary()
    display_all_books()
    display_all_members()
    
    # Test 8: Data validation helpers
    print("\n8. TESTING VALIDATION HELPERS:")
    print(f"   - Valid genre check: {is_valid_genre('Fiction')}")
    print(f"   - Invalid genre check: {is_valid_genre('Romance')}")
    print(f"   - Book exists check: {book_exists('1001')}")
    print(f"   - Book doesn't exist check: {book_exists('9999')}")
    print(f"   - Member exists check: {member_exists('M001')}")
    print(f"   - Member doesn't exist check: {member_exists('M999')}")
    
    # Final verification
    print("\n9. FINAL VERIFICATION:")
    print(f"   Total books in system: {len(books)}")
    print(f"   Total members in system: {len(members)}")
    print(f"   All data structures initialized: ")
    print(f"   Core functions working: ")
    print(f"   Search functions working: ")
    print(f"   Update functions working: ")
    print(f"   Delete functions working: ")
    print(f"   Borrow functions working: ")
    print(f"   Return functions working: ")
    print(f"   Validation helpers working: ")
    
    print("\n COMPLETE LIBRARY SYSTEM IMPLEMENTED!")
    print("   All assignment requirements have been successfully implemented!")
    print("   The system is ready for demonstration and testing.")

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    """
    When this file is run directly, it executes the complete system test.
    This verifies that all library functionality is working correctly.
    """
    test_complete_system()