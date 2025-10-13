"""
Login Helper Script
This script helps you log in with the correct hashed passwords
"""

from operations import *
import hashlib

def hash_password(password):
    """Hash passwords using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def show_password_hashes():
    """Show what the password hashes should be"""
    print("PASSWORD HASHES FOR TESTING:")
    print("=" * 50)
    
    test_passwords = {
        "admin123": "admin123",
        "lib123": "lib123",
        "pass123": "pass123"
    }
    
    for plain, hashed in test_passwords.items():
        print(f"Plain: {plain} -> Hash: {hashed}")
    
    print("\nCURRENT USER DATABASE:")
    print("=" * 50)
    for username, user_data in users.items():
        print(f"Username: {username}")
        print(f"  Role: {user_data['role']}")
        print(f"  Stored Hash: {user_data['password']}")
        print(f"  Full Name: {user_data['full_name']}")
        print()

def reset_passwords_to_plain_text():
    """Reset passwords to use plain text for testing (temporarily)"""
    print("RESETTING PASSWORDS TO PLAIN TEXT FOR TESTING...")
    
    # Update passwords to plain text
    users["admin"]["password"] = "admin123"
    users["librarian1"]["password"] = "lib123" 
    users["alice"]["password"] = "pass123"
    users["bob"]["password"] = "pass123"
    
    # Save the changes
    save_data()
    print("Passwords reset to plain text successfully!")
    print("You can now login with:")
    print("  admin / admin123")
    print("  librarian1 / lib123")
    print("  alice / pass123")
    print("  bob / pass123")

def test_logins():
    """Test all logins with current password setup"""
    print("TESTING LOGINS WITH CURRENT SETUP:")
    print("=" * 50)
    
    test_accounts = [
        ("admin", "admin123"),
        ("librarian1", "lib123"),
        ("alice", "pass123"),
        ("bob", "pass123")
    ]
    
    for username, password in test_accounts:
        print(f"\nTesting {username}:")
        if login(username, password):
            print(f"  SUCCESS - Logged in as {current_user['role']}")
            logout()
        else:
            print(f"  FAILED - Check password hash")

if __name__ == "__main__":
    print("LOGIN HELPER UTILITY")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. Show password hashes")
        print("2. Reset passwords to plain text (recommended for testing)")
        print("3. Test all logins")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            show_password_hashes()
            
        elif choice == "2":
            reset_passwords_to_plain_text()
            
        elif choice == "3":
            test_logins()
            
        elif choice == "4":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice")