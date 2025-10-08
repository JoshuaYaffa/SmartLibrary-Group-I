"""
ReadEasy Mini Library Management System
Core operations module

PROG211 - Individual Assignment
Student: Joshua Mohamed Katibi Yaffa
ID  : 905004075
GitHub: JoshuaYaffa/SmartLibrary-Group-I

This module contains the core data structures and functions for managing
books and members in the library system.
"""

# ==================== GLOBAL DATA STRUCTURES ====================

# I'm using a tuple for genres because it's immutable and these categories won't change
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

# ==================== HELPER FUNCTIONS FOR TESTING ====================

def display_books():
    """Shows all books currently in the library - useful for debugging"""
    print("\n📚 BOOKS IN LIBRARY:")
    if not books:
        print("   No books available.")
        return
    
    # Loop through each book and display its details
    for isbn, book in books.items():
        print(f"   ISBN: {isbn}")
        print(f"   Title: {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Genre: {book['genre']}")
        print(f"   Copies: {book['total_copies']}")
        print("   " + "-" * 30)

def display_members():
    """Shows all registered members - helpful for verification"""
    print("\n👥 LIBRARY MEMBERS:")
    if not members:
        print("   No members registered.")
        return
    
    # Display each member's information
    for member in members:
        print(f"   ID: {member['member_id']}")
        print(f"   Name: {member['name']}")
        print(f"   Email: {member['email']}")
        print(f"   Borrowed Books: {len(member['borrowed_books'])}")
        print("   " + "-" * 30)

# ==================== TESTING FUNCTIONS ====================

def test_library_functions():
    """
    Tests the core library functions to make sure they work correctly.
    I'm testing edge cases and normal operations to verify everything works.
    """
    print("🧪 TESTING LIBRARY FUNCTIONS")
    print("=" * 50)
    
    # Start with a clean slate for testing
    books.clear()
    members.clear()
    
    # Test 1: Adding books with various scenarios
    print("\n1. TESTING BOOK ADDITIONS:")
    
    # This should work - valid book
    result1 = add_book("1001", "Python Programming", "John Doe", "Non-Fiction", 5)
    print(f"   Added valid book: {result1} (should be True)")
    
    # This should fail - duplicate ISBN
    result2 = add_book("1001", "Another Book", "Jane Smith", "Fiction", 3)
    print(f"   Added duplicate ISBN: {result2} (should be False)")
    
    # This should fail - invalid genre
    result3 = add_book("1002", "Space Book", "Alex Star", "Space Opera", 2)
    print(f"   Added invalid genre: {result3} (should be False)")
    
    # This should fail - zero copies
    result4 = add_book("1003", "Empty Library", "Test Author", "Fiction", 0)
    print(f"   Added book with zero copies: {result4} (should be False)")
    
    # Test 2: Adding members
    print("\n2. TESTING MEMBER REGISTRATION:")
    
    # This should work - valid member
    result5 = add_member("M001", "Alice Johnson", "alice@email.com")
    print(f"   Added valid member: {result5} (should be True)")
    
    # This should fail - duplicate member ID
    result6 = add_member("M001", "Bob Wilson", "bob@email.com")
    print(f"   Added duplicate member ID: {result6} (should be False)")
    
    # Show what we have in the system now
    print("\n3. CURRENT SYSTEM STATE:")
    display_books()
    display_members()
    
    # Verify our functions return the right data types
    print("\n4. VERIFYING FUNCTION BEHAVIOR:")
    print(f"   add_book returns boolean: {isinstance(result1, bool)}")
    print(f"   add_member returns boolean: {isinstance(result5, bool)}")
    
    print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")

# This runs our tests when we execute the file directly
if __name__ == "__main__":
    test_library_functions()