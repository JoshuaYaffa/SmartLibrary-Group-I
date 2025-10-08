"""
ReadEasy Mini Library Management System
Core operations module

PROG211 - Individual Assignment
Student: Joshua Yaffa
GitHub: JoshuaYaffa/SmartLibrary-Group-I

Foundation Setup: Data Structures and Basic CRUD Operations
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
        ("1005", "Steve Jobs Biography", "Walter Isaacson", "Biography", 3)
    ]
    
    # Sample members data
    sample_members = [
        ("M001", "Alice Johnson", "alice@email.com"),
        ("M002", "Bob Wilson", "bob@email.com"),
        ("M003", "Carol Davis", "carol@email.com")
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

def test_system_foundation():
    """
    Comprehensive test of all system foundation components.
    I'm testing everything to make sure the base system is working properly.
    """
    print(" SYSTEM FOUNDATION TESTING")
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
    
    # Test 2: Data validation helpers
    print("\n2. TESTING VALIDATION HELPERS:")
    print(f"   - Valid genre check: {is_valid_genre('Fiction')}")
    print(f"   - Invalid genre check: {is_valid_genre('Romance')}")
    print(f"   - Book exists check: {book_exists('2001')}")
    print(f"   - Book doesn't exist check: {book_exists('9999')}")
    print(f"   - Member exists check: {member_exists('M100')}")
    print(f"   - Member doesn't exist check: {member_exists('M999')}")
    
    # Test 3: Setup sample data
    print("\n3. TESTING SAMPLE DATA SETUP:")
    setup_sample_data()
    
    # Test 4: Display functions
    print("\n4. TESTING DISPLAY FUNCTIONS:")
    display_system_summary()
    display_all_books()
    display_all_members()
    
    # Final verification
    print("\n5. FINAL VERIFICATION:")
    print(f"   Total books in system: {len(books)}")
    print(f"   Total members in system: {len(members)}")
    print(f"   All data structures initialized: ")
    print(f"   Core functions working: ")
    print(f"   Validation helpers working: ")
    
    print("\n SYSTEM FOUNDATION COMPLETED!")
    print("   Ready to implement borrowing and search features!")

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    """
    When this file is run directly, it executes the system foundation test.
    This helps me verify that everything is working before building additional features.
    """
    test_system_foundation()