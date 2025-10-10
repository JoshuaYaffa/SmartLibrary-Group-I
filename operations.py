"""
ReadEasy Mini Library Management System
Core operations module with Enhanced Features

PROG211 - Individual Assignment
Student: Joshua Mohamed Katibi Yaffa
ID: 905004075
Class : BSEM1101
Semseter: 3
Year : 2
GitHub: JoshuaYaffa/SmartLibrary-Group-I

Complete Library System with Security, Audit Trail, and Advanced Features
"""

import datetime
import json
import os
import time
import hashlib

# ==================== ENHANCED SECURITY SYSTEM WITH AUDIT TRAIL ====================

# Audit trail storage
audit_trail = {
    "members": [],
    "admins": [], 
    "librarians": []
}

# User roles and permissions
USER_ROLES = {
    "admin": ["add_member", "delete_member", "add_book", "delete_book", "update_book", 
              "update_member", "search_books", "borrow_book", "return_book", "view_system",
              "view_audit_trail", "system_backup", "system_health", "data_export", "batch_operations"],
    "librarian": ["add_book", "search_books", "borrow_book", "return_book", "view_system", "batch_operations"],
    "member": ["search_books", "borrow_book", "return_book", "view_own_data", "change_password"]
}

# User database (with hashed passwords)
users = {
    "admin": {
        "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
        "role": "admin", 
        "member_id": "ADMIN001", 
        "full_name": "System Administrator",
        "email": "admin@readeasy.com"
    },
    "librarian1": {
        "password": "2b6722a4afd6b117b35d9d5a5d46c3c0c5c14e4e1e4d2a2a2a2a2a2a2a2a2a2a",
        "role": "librarian", 
        "member_id": "LIB001", 
        "full_name": "Sarah Librarian",
        "email": "sarah@readeasy.com"
    },
    "alice": {
        "password": "d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1",
        "role": "member", 
        "member_id": "M001", 
        "full_name": "Alice Johnson",
        "email": "alice@email.com"
    },
    "bob": {
        "password": "d74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1",
        "role": "member", 
        "member_id": "M002", 
        "full_name": "Bob Wilson",
        "email": "bob@email.com"
    }
}

# Global data structures
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery", "Biography")
books = {}
members = []

# Current user session and activity tracking
current_user = None
last_activity_time = None
DATA_FILE = "library_data.json"

# ==================== PERSISTENT DATA STORAGE ====================

def hash_password(password):
    """Hash passwords using SHA-256 for basic security"""
    return hashlib.sha256(password.encode()).hexdigest()

def save_data():
    """Save all system data to JSON file for persistence"""
    try:
        data = {
            'books': books,
            'members': members,
            'audit_trail': audit_trail,
            'users': users,
            'last_save': datetime.datetime.now().isoformat()
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        if current_user:
            log_audit_event(
                current_user["role"],
                current_user["username"],
                current_user["full_name"],
                "DATA_SAVE",
                "System data saved successfully"
            )
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_data():
    """Load system data from JSON file"""
    global books, members, audit_trail, users
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                books.update(data.get('books', {}))
                members.extend(data.get('members', []))
                
                # Merge audit trails to preserve current session + loaded data
                loaded_audit = data.get('audit_trail', {'admins': [], 'librarians': [], 'members': []})
                for role in audit_trail:
                    audit_trail[role].extend(loaded_audit.get(role, []))
                
                users.update(data.get('users', {}))
            
            print("System data loaded successfully")
            return True
    except Exception as e:
        print(f"Error loading data: {e}")
    return False

# ==================== SESSION MANAGEMENT ====================

def get_current_timestamp():
    """Get formatted current timestamp for audit trail"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def update_activity():
    """Update last activity time for session management"""
    global last_activity_time
    last_activity_time = time.time()

def check_session_timeout():
    """Automatically log out inactive users after 30 minutes"""
    global current_user, last_activity_time
    if current_user and last_activity_time:
        if time.time() - last_activity_time > 1800:
            print("Session timed out due to inactivity")
            logout()
            return True
    return False

def log_audit_event(user_role, username, full_name, action, details=""):
    """Log an event to the audit trail with complete details"""
    timestamp = get_current_timestamp()
    event = {
        "timestamp": timestamp,
        "username": username,
        "full_name": full_name,
        "action": action,
        "details": details,
        "date": timestamp.split()[0],
        "time": timestamp.split()[1],
    }
    
    # Categorize by role
    if user_role == "admin":
        audit_trail["admins"].append(event)
    elif user_role == "librarian":
        audit_trail["librarians"].append(event)
    elif user_role == "member":
        audit_trail["members"].append(event)
    else:
        audit_trail["admins"].append(event)
    
    print(f"[AUDIT] {timestamp} - {user_role.upper()} {username}: {action}")
    save_data()

def login(username, password):
    """Authenticate users and establish a session with audit logging"""
    global current_user, last_activity_time
    
    hashed_input = hash_password(password)
    
    if username in users and users[username]["password"] == hashed_input:
        current_user = {
            "username": username,
            "role": users[username]["role"],
            "member_id": users[username]["member_id"],
            "full_name": users[username]["full_name"],
            "email": users[username]["email"]
        }
        last_activity_time = time.time()
        
        log_audit_event(
            current_user["role"],
            username,
            current_user["full_name"],
            "LOGIN",
            "User logged in successfully"
        )
        
        print(f"Login successful! Welcome {username} ({current_user['role']} role)")
        return True
    else:
        print("Login failed: Invalid username or password")
        log_audit_event(
            "unknown",
            username,
            "Unknown User",
            "FAILED_LOGIN_ATTEMPT",
            "Invalid credentials provided"
        )
        return False

def logout():
    """End the current user session with audit logging"""
    global current_user, last_activity_time
    if current_user:
        log_audit_event(
            current_user["role"],
            current_user["username"],
            current_user["full_name"],
            "LOGOUT",
            f"Session duration: {int(time.time() - last_activity_time)} seconds"
        )
        print(f"Goodbye {current_user['username']}!")
        current_user = None
        last_activity_time = None
    else:
        print("No user is currently logged in")

def get_current_user():
    """Get information about the currently logged-in user"""
    return current_user

# ==================== SECURITY & PERMISSIONS ====================

def check_permission(operation):
    """Check if the current user has permission to perform an operation"""
    if not current_user:
        print("Access denied: Please log in first")
        return False
    
    update_activity()
    
    user_role = current_user["role"]
    
    if operation in USER_ROLES[user_role]:
        return True
    else:
        print(f"Access denied: {user_role} role cannot perform '{operation}' operation")
        return False

def require_permission(operation):
    """Decorator function to protect other functions with permission checks and audit logging"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if check_permission(operation):
                if current_user:
                    action_name = func.__name__.upper().replace('_', ' ')
                    
                    details_parts = []
                    if args:
                        details_parts.append(f"Args: {args}")
                    if kwargs:
                        details_parts.append(f"Kwargs: {kwargs}")
                    details = " | ".join(details_parts) if details_parts else "No additional parameters"
                    
                    log_audit_event(
                        current_user["role"],
                        current_user["username"],
                        current_user["full_name"],
                        action_name,
                        details
                    )
                
                result = func(*args, **kwargs)
                save_data()
                return result
            else:
                return False
        return wrapper
    return decorator

# ==================== DATA VALIDATION ENHANCEMENTS ====================

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[-1] and len(email) > 5

def validate_isbn(isbn):
    """Basic ISBN validation"""
    clean_isbn = isbn.replace('-', '').replace(' ', '')
    return clean_isbn.isalnum() and len(clean_isbn) in [10, 13]

def validate_phone(phone):
    """Basic phone number validation"""
    clean_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    return clean_phone.isdigit() and len(clean_phone) >= 10

# ==================== CORE LIBRARY FUNCTIONS ====================

@require_permission("add_book")
def add_book(isbn, title, author, genre, total_copies):
    """Add a new book to the library with enhanced validation"""
    if not validate_isbn(isbn):
        print("Error: Invalid ISBN format")
        return False
        
    if isbn in books:
        print(f"Error: Book with ISBN {isbn} already exists!")
        return False
    
    if genre not in GENRES:
        print(f"Error: Genre '{genre}' is not valid. Valid genres: {GENRES}")
        return False
    
    if total_copies < 1:
        print("Error: Total copies must be at least 1")
        return False
    
    books[isbn] = {
        "title": title,
        "author": author, 
        "genre": genre,
        "total_copies": total_copies,
        "date_added": get_current_timestamp()
    }
    
    print(f"Successfully added book: '{title}' by {author}")
    return True

@require_permission("add_member")
def add_member(member_id, name, email, phone=""):
    """Register a new member with enhanced validation"""
    if not validate_email(email):
        print("Error: Invalid email format")
        return False
        
    if phone and not validate_phone(phone):
        print("Error: Invalid phone number format")
        return False
    
    for member in members:
        if member["member_id"] == member_id:
            print(f"Error: Member with ID {member_id} already exists!")
            return False
    
    new_member = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "phone": phone,
        "borrowed_books": [],
        "date_registered": get_current_timestamp()
    }
    members.append(new_member)
    
    print(f"Successfully added member: {name} ({member_id})")
    return True

@require_permission("search_books")
def search_books(query, by="title"):
    """Search for books by title or author"""
    matching_books = []
    search_term = query.lower()
    
    for isbn, book in books.items():
        if by == "title":
            if search_term in book["title"].lower():
                matching_books.append(book)
        elif by == "author":
            if search_term in book["author"].lower():
                matching_books.append(book)
        else:
            print(f"Error: Cannot search by '{by}'. Use 'title' or 'author'.")
            return []
    
    return matching_books

@require_permission("update_book")
def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """Update specific fields of an existing book"""
    if isbn not in books:
        return False
    
    book = books[isbn]
    
    if title is not None:
        book["title"] = title
    
    if author is not None:
        book["author"] = author
    
    if genre is not None:
        if genre not in GENRES:
            return False
        book["genre"] = genre
    
    if total_copies is not None:
        if total_copies < 0:
            return False
        book["total_copies"] = total_copies
    
    book["last_updated"] = get_current_timestamp()
    return True

@require_permission("update_member")
def update_member(member_id, name=None, email=None, phone=None):
    """Update specific fields of an existing member"""
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        return False
    
    if name is not None:
        member["name"] = name
    
    if email is not None:
        if not validate_email(email):
            return False
        member["email"] = email
    
    if phone is not None:
        if not validate_phone(phone):
            return False
        member["phone"] = phone
    
    return True

@require_permission("delete_book")
def delete_book(isbn):
    """Remove a book from the library system"""
    if isbn not in books:
        return False
    
    for member in members:
        if isbn in member["borrowed_books"]:
            return False
    
    del books[isbn]
    return True

@require_permission("delete_member")
def delete_member(member_id):
    """Remove a member from the library system"""
    member = None
    member_index = -1
    for index, m in enumerate(members):
        if m["member_id"] == member_id:
            member = m
            member_index = index
            break
    
    if member is None:
        return False
    
    if len(member["borrowed_books"]) > 0:
        return False
    
    del members[member_index]
    return True

@require_permission("borrow_book")
def borrow_book(isbn, member_id):
    """Allow a member to borrow a book from the library"""
    if isbn not in books:
        print(f"Book with ISBN {isbn} not found.")
        return False
    
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        print(f"Member with ID {member_id} not found.")
        return False
    
    if books[isbn]["total_copies"] <= 0:
        print(f"No copies available for '{books[isbn]['title']}'.")
        return False
    
    if len(member["borrowed_books"]) >= 3:
        print(f"{member['name']} has reached the borrowing limit of 3 books.")
        return False
    
    if isbn in member["borrowed_books"]:
        print(f"{member['name']} already has this book borrowed.")
        return False
    
    books[isbn]["total_copies"] -= 1
    member["borrowed_books"].append(isbn)
    
    print(f"{member['name']} successfully borrowed '{books[isbn]['title']}'")
    return True

@require_permission("return_book")
def return_book(isbn, member_id):
    """Allow a member to return a borrowed book to the library"""
    if isbn not in books:
        print(f"Book with ISBN {isbn} not found.")
        return False
    
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        print(f"Member with ID {member_id} not found.")
        return False
    
    if isbn not in member["borrowed_books"]:
        print(f"{member['name']} doesn't have this book borrowed.")
        return False
    
    books[isbn]["total_copies"] += 1
    member["borrowed_books"].remove(isbn)
    
    print(f"{member['name']} successfully returned '{books[isbn]['title']}'")
    return True

def get_member_borrowed_books(member_id):
    """Get detailed information about books a member has borrowed"""
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    
    if member is None:
        return []
    
    borrowed_details = []
    for isbn in member["borrowed_books"]:
        if isbn in books:
            book_info = books[isbn].copy()
            book_info["isbn"] = isbn
            borrowed_details.append(book_info)
    
    return borrowed_details

# ==================== ADVANCED FEATURES ====================

@require_permission("batch_operations")
def batch_add_books(book_list):
    """Add multiple books at once"""
    success_count = 0
    total_books = len(book_list)
    
    for book_data in book_list:
        if len(book_data) == 5 and add_book(*book_data):
            success_count += 1
    
    log_audit_event(
        current_user["role"],
        current_user["username"],
        current_user["full_name"],
        "BATCH_ADD_BOOKS",
        f"Added {success_count}/{total_books} books successfully"
    )
    
    print(f"Batch operation complete: {success_count}/{total_books} books added")
    return success_count

@require_permission("system_backup")
def create_backup():
    """Create a timestamped backup of all system data"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_library_{timestamp}.json"
    
    data = {
        'books': books,
        'members': members,
        'audit_trail': audit_trail,
        'users': users,
        'backup_timestamp': timestamp,
        'backup_created_by': current_user['username'] if current_user else 'system'
    }
    
    try:
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        log_audit_event(
            current_user["role"],
            current_user["username"],
            current_user["full_name"],
            "SYSTEM_BACKUP",
            f"Backup created: {backup_file} with {len(books)} books and {len(members)} members"
        )
        
        print(f"Backup created successfully: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

@require_permission("system_health")
def system_health_check():
    """Check system health and data integrity"""
    print("\n" + "=" * 60)
    print("SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    for member in members:
        for isbn in member['borrowed_books']:
            if isbn not in books:
                issues.append(f"Orphaned book {isbn} borrowed by {member['name']}")
    
    for isbn, book in books.items():
        if book['total_copies'] < 0:
            issues.append(f"Negative copies for book '{book['title']}' ({isbn})")
        elif book['total_copies'] == 0:
            warnings.append(f"Zero copies available for '{book['title']}' ({isbn})")
    
    for member in members:
        if not validate_email(member['email']):
            warnings.append(f"Invalid email format for member {member['name']}")
    
    if issues:
        print("CRITICAL ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No critical issues found")
    
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("No warnings")
    
    print(f"SYSTEM STATISTICS:")
    print(f"  - Total books: {len(books)}")
    print(f"  - Total members: {len(members)}")
    print(f"  - Total audit events: {sum(len(v) for v in audit_trail.values())}")
    print(f"  - Available genres: {len(GENRES)}")
    
    total_borrowed = sum(len(member['borrowed_books']) for member in members)
    print(f"  - Currently borrowed books: {total_borrowed}")
    
    return len(issues) == 0

@require_permission("data_export")
def export_books_to_csv():
    """Export book catalog to CSV format"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"library_books_export_{timestamp}.csv"
        
        with open(filename, 'w') as f:
            f.write("ISBN,Title,Author,Genre,Available Copies,Date Added\n")
            for isbn, book in books.items():
                f.write(f'"{isbn}","{book["title"]}","{book["author"]}","{book["genre"]}",{book["total_copies"]},"{book.get("date_added", "Unknown")}"\n')
        
        log_audit_event(
            current_user["role"],
            current_user["username"],
            current_user["full_name"],
            "DATA_EXPORT",
            f"Exported {len(books)} books to {filename}"
        )
        
        print(f"Export successful: {filename}")
        return filename
    except Exception as e:
        print(f"Export failed: {e}")
        return None

@require_permission("change_password")
def change_password(old_password, new_password):
    """Allow users to change their password"""
    if not current_user:
        return False
    
    username = current_user['username']
    hashed_old = hash_password(old_password)
    hashed_new = hash_password(new_password)
    
    if users[username]["password"] == hashed_old:
        users[username]["password"] = hashed_new
        
        log_audit_event(
            current_user["role"],
            current_user["username"],
            current_user["full_name"],
            "PASSWORD_CHANGE",
            "Password updated successfully"
        )
        
        save_data()
        print("Password changed successfully")
        return True
    else:
        print("Current password is incorrect")
        return False

def send_overdue_notifications():
    """Send notifications for borrowed books (simulated)"""
    print("SENDING BORROWED BOOK NOTIFICATIONS:")
    notification_count = 0
    
    for member in members:
        borrowed_count = len(member['borrowed_books'])
        if borrowed_count > 0:
            print(f"  Notification sent to {member['name']}: {borrowed_count} book(s) currently borrowed")
            notification_count += 1
            
            log_audit_event(
                "system",
                "system",
                "Automated System",
                "BORROWED_BOOK_NOTIFICATION",
                f"Sent to {member['name']} about {borrowed_count} borrowed books"
            )
    
    if notification_count == 0:
        print("  No borrowed books to notify about")
    
    return notification_count

# ==================== AUDIT TRAIL VIEWING FUNCTIONS ====================

@require_permission("view_audit_trail")
def display_audit_trail(role_filter=None):
    """Display the complete audit trail, optionally filtered by role"""
    check_session_timeout()
    
    print("\n" + "=" * 80)
    print("                         AUDIT TRAIL REPORT")
    print("=" * 80)
    
    total_events = 0
    roles_to_show = [role_filter] if role_filter and role_filter in audit_trail else ["admins", "librarians", "members"]
    
    for role in roles_to_show:
        events = audit_trail[role]
        if events:
            print(f"{role.upper()} ACTIVITIES ({len(events)} events):")
            print("-" * 80)
            
            for event in events[-10:]:
                print(f"  Date: {event['date']} | Time: {event['time']}")
                print(f"  User: {event['full_name']} ({event['username']})")
                print(f"  Action: {event['action']}")
                if event['details'] and len(event['details']) < 100:
                    print(f"  Details: {event['details']}")
                print("-" * 40)
            
            total_events += len(events)
    
    print(f"Total events displayed: {total_events}")
    print("=" * 80)

@require_permission("view_audit_trail")
def generate_security_report():
    """Generate comprehensive security report"""
    print("\n" + "=" * 70)
    print("                   SECURITY ANALYSIS REPORT")
    print("=" * 70)
    
    all_events = []
    for role_events in audit_trail.values():
        all_events.extend(role_events)
    
    failed_logins = [e for e in all_events if "FAILED_LOGIN" in e["action"]]
    
    user_activity = {}
    for event in all_events:
        user_activity[event['username']] = user_activity.get(event['username'], 0) + 1
    
    most_active_user = max(user_activity.items(), key=lambda x: x[1]) if user_activity else ("None", 0)
    
    action_counts = {}
    for event in all_events:
        action_counts[event['action']] = action_counts.get(event['action'], 0) + 1
    
    most_common_action = max(action_counts.items(), key=lambda x: x[1]) if action_counts else ("None", 0)
    
    print("SECURITY METRICS:")
    print(f"  - Total events recorded: {len(all_events)}")
    print(f"  - Failed login attempts: {len(failed_logins)}")
    print(f"  - Most active user: {most_active_user[0]} ({most_active_user[1]} actions)")
    print(f"  - Most common action: {most_common_action[0]} ({most_common_action[1]} times)")
    print(f"  - Unique users: {len(user_activity)}")
    
    recent_failed_logins = [e for e in failed_logins if e['timestamp'] > get_current_timestamp().split()[0]]
    
    if recent_failed_logins:
        print("RECENT SECURITY EVENTS (Today):")
        for event in recent_failed_logins[-5:]:
            print(f"  - {event['timestamp']}: Failed login attempt by {event['username']}")
    
    print("ROLE DISTRIBUTION:")
    for role, events in audit_trail.items():
        print(f"  - {role.upper():<12}: {len(events):>4} events")
    
    print("=" * 70)

def display_my_activity():
    """Users can view their own activity history"""
    if not current_user:
        print("Please log in to view your activity")
        return
    
    user_events = []
    for role_events in audit_trail.values():
        for event in role_events:
            if event['username'] == current_user['username']:
                user_events.append(event)
    
    user_events.sort(key=lambda x: x['timestamp'], reverse=True)
    
    if not user_events:
        print("No activity found for your account")
        return
    
    print(f"YOUR ACTIVITY HISTORY ({len(user_events)} most recent events):")
    print("=" * 70)
    
    for event in user_events[:10]:
        print(f"Date: {event['date']} | Time: {event['time']}")
        print(f"Action: {event['action']}")
        if event['details'] and len(event['details']) < 80:
            print(f"Details: {event['details']}")
        print("-" * 40)

# ==================== DISPLAY FUNCTIONS ====================

@require_permission("view_system")
def display_all_books():
    """Shows all books in the library"""
    print("\nLIBRARY BOOK COLLECTION:")
    print("=" * 60)
    
    if not books:
        print("No books in the library yet.")
        return
    
    for book_number, (isbn, book) in enumerate(books.items(), 1):
        print(f"{book_number}. ISBN: {isbn}")
        print(f"   Title: {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Genre: {book['genre']}")
        print(f"   Copies Available: {book['total_copies']}")
        if 'date_added' in book:
            print(f"   Added: {book['date_added']}")
        print()

@require_permission("view_system")
def display_all_members():
    """Shows all registered members"""
    print("\nREGISTERED LIBRARY MEMBERS:")
    print("=" * 60)
    
    if not members:
        print("No members registered yet.")
        return
    
    for member_number, member in enumerate(members, 1):
        print(f"{member_number}. ID: {member['member_id']}")
        print(f"   Name: {member['name']}")
        print(f"   Email: {member['email']}")
        if member['phone']:
            print(f"   Phone: {member['phone']}")
        print(f"   Books Borrowed: {len(member['borrowed_books'])}")
        if 'date_registered' in member:
            print(f"   Registered: {member['date_registered']}")
        print()

@require_permission("view_system")
def display_system_summary():
    """Shows a quick overview of the entire system"""
    print("\nSYSTEM SUMMARY:")
    print("=" * 40)
    print(f"Total Books: {len(books)}")
    print(f"Total Members: {len(members)}")
    print(f"Available Genres: {len(GENRES)}")
    
    total_borrowed = sum(len(member['borrowed_books']) for member in members)
    total_copies = sum(book['total_copies'] for book in books.values())
    
    print(f"Total Copies Available: {total_copies}")
    print(f"Currently Borrowed: {total_borrowed}")
    print(f"System Uptime: Loaded {len(audit_trail['admins']) + len(audit_trail['librarians']) + len(audit_trail['members'])} audit events")
    print("=" * 40)

def display_search_results(books_list, search_type, query):
    """Display search results in a user-friendly format"""
    if not books_list:
        print(f"No books found with {search_type} containing '{query}'")
        return
    
    print(f"SEARCH RESULTS: {len(books_list)} books with {search_type} containing '{query}'")
    print("=" * 60)
    
    for book_number, book in enumerate(books_list, 1):
        print(f"{book_number}. Title: {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Genre: {book['genre']}")
        print(f"   Copies Available: {book['total_copies']}")
        print()

def display_borrowed_books(member_id):
    """Display all books currently borrowed by a specific member"""
    borrowed_books = get_member_borrowed_books(member_id)
    
    member_name = "Unknown"
    for member in members:
        if member["member_id"] == member_id:
            member_name = member["name"]
            break
    
    print(f"BOOKS BORROWED BY {member_name} ({member_id}):")
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

# ==================== INITIALIZATION ====================

def initialize_system():
    """Initialize the system by loading saved data"""
    print("Initializing ReadEasy Library System...")
    load_data()
    print("System ready!")

# Initialize when module is imported
initialize_system()