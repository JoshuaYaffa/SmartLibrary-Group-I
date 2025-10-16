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
# Security and Audit Module with Enhanced Features
#
# GitHub: JoshuaYaffa/SmartLibrary-Group-I
# ================================================

"""
This module handles all security and audit-related operations for the system.
It manages user authentication, roles, login tracking, and audit logs.
All logins, logouts, and major system actions are recorded with timestamps.
"""

import datetime
import os

# ==============================
# Global Variables
# ==============================

current_user = None  # Stores currently logged-in user details

# Directory for storing logs
LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

AUDIT_LOG_FILE = os.path.join(LOG_FOLDER, "audit_log.txt")
ERROR_LOG_FILE = os.path.join(LOG_FOLDER, "error_log.txt")

# ==============================
# Predefined Users and Roles
# ==============================

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}


# ==============================
# Logging Functions
# ==============================

def log_event(username, action):
    """Records a user action into the audit log with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] USER: {username} - ACTION: {action}\n")


def log_error(message):
    """Records any system error or exception."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] ERROR: {message}\n")


# ==============================
# Authentication System
# ==============================

def authenticate():
    """
    Handles user login for Admin, Staff, and Members.
    Admin and Staff must provide username and password.
    Members can log in using only their name.
    """
    global current_user

    print("=== Select Role ===")
    print("1. Admin")
    print("2. Staff")
    print("3. Member")

    role_choice = input("Enter your choice (1/2/3): ").strip()

    if role_choice == "1":
        role = "admin"
    elif role_choice == "2":
        role = "staff"
    elif role_choice == "3":
        role = "member"
    else:
        print("Invalid selection.")
        return False

    # Member login (name only)
    if role == "member":
        username = input("Enter your name: ").strip()
        if not username:
            print("Invalid name. Please try again.")
            return False
        current_user = {"username": username, "role": role}
        log_event(username, "Logged in as member")
        print(f"Welcome, {username}! Role: Member")
        return True

    # Admin or Staff login (with password)
    print(f"=== Login as {role.capitalize()} ===")
    for attempt in range(3):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username in USERS and USERS[username]["password"] == password and USERS[username]["role"] == role:
            current_user = {"username": username, "role": role}
            log_event(username, f"Logged in successfully as {role}")
            print(f"Welcome, {username}! Role: {role.capitalize()}")
            return True
        else:
            print("Invalid credentials. Try again.")

    print("Too many failed attempts. Exiting system.")
    return False


def logout():
    """Handles user logout and logs it in the audit trail."""
    global current_user
    if current_user:
        username = current_user["username"]
        log_event(username, "Logged out")
        print(f"Goodbye, {username}. You have been logged out.")
        current_user = None
    else:
        print("No user is currently logged in.")


# ==============================
# Access Control
# ==============================

def has_access(required_role):
    """
    Checks if the current user has permission to perform a specific action.
    Admins have full access; staff and members are restricted.
    """
    if not current_user:
        print("Access denied. Please log in first.")
        return False

    user_role = current_user["role"]
    if user_role == required_role or user_role == "admin":
        return True
    else:
        print(f"Access denied. This action requires {required_role} privileges.")
        return False


# ==============================
# Log Viewing Functions (Admin Only)
# ==============================

def view_audit_log():
    """Allows admin to view the system audit trail."""
    if not has_access("admin"):
        return
    print("\n=== Audit Log ===")
    try:
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as log_file:
            content = log_file.read()
            if content.strip():
                print(content)
            else:
                print("No audit logs recorded yet.")
    except FileNotFoundError:
        print("Audit log file not found.")


def view_error_log():
    """Allows admin to view all recorded errors."""
    if not has_access("admin"):
        return
    print("\n=== Error Log ===")
    try:
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as log_file:
            content = log_file.read()
            if content.strip():
                print(content)
            else:
                print("No errors logged yet.")
    except FileNotFoundError:
        print("Error log file not found.")


# ==============================
# Module Test Section (Optional)
# ==============================

if __name__ == "__main__":
    print("Running security module test...\n")
    if authenticate():
        log_event(current_user["username"], "Test event - security module operational")
        view_audit_log()
        logout()
