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
This file handles all the security and audit features of my Mini Library Management System.
It manages user authentication, roles, logging, and audit trails.
All user actions such as login, logout, and system updates are recorded with date and time.
"""

import datetime
import os

# ==============================
# Global Variables
# ==============================

# This variable stores the currently logged-in user information
current_user = None

# The folder where log files are stored
LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# File paths for logs
AUDIT_LOG_FILE = os.path.join(LOG_FOLDER, "audit_log.txt")
ERROR_LOG_FILE = os.path.join(LOG_FOLDER, "error_log.txt")

# ==============================
# Predefined Users and Roles
# ==============================

# For this system, I created two user roles: admin and staff.
# Each user is represented by a dictionary containing username, password, and role.
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"}
}


# ==============================
# Logging Functions
# ==============================

def log_event(username, action):
    """
    Records every significant system event in the audit log file.
    Each entry includes the username, the action performed, and the timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] USER: {username} - ACTION: {action}\n")


def log_error(message):
    """
    Records system errors or exceptions into a separate error log file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] ERROR: {message}\n")


# ==============================
# Authentication Functions
# ==============================

def authenticate():
    """
    Handles user login.
    A user has three attempts to enter the correct username and password.
    After a successful login, user details are stored in the global variable current_user.
    """
    global current_user

    print("=== Login Required ===")
    for attempt in range(3):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            current_user = {"username": username, "role": role}
            log_event(username, "Logged in successfully")
            print(f"Welcome, {username}! Role: {role.capitalize()}")
            return True
        else:
            print("Invalid username or password. Try again.")

    print("Too many failed attempts. Exiting system.")
    return False


def logout():
    """
    Handles user logout.
    The event is also recorded in the audit trail with timestamp.
    """
    global current_user
    if current_user:
        username = current_user["username"]
        log_event(username, "Logged out")
        print(f"Goodbye, {username}. You have been logged out.")
        current_user = None
    else:
        print("No user is currently logged in.")


# ==============================
# Role-Based Access Control
# ==============================

def has_access(required_role):
    """
    Checks if the currently logged-in user has the required role.
    Returns True if authorized, otherwise False.
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
# Utility Function for Viewing Logs
# ==============================

def view_audit_log():
    """
    Allows an admin user to view the audit trail file directly from the system.
    """
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
        print("No audit log file found.")


def view_error_log():
    """
    Allows an admin user to view all recorded errors.
    """
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
        print("No error log file found.")


# ==============================
# Test Section (Optional)
# ==============================

if __name__ == "__main__":
    print("Running security module test...\n")
    if authenticate():
        log_event(current_user["username"], "Test event - security module operational")
        view_audit_log()
        logout()
