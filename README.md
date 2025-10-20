
ReadEasy Mini Library Management System
Instructions on How to Run the Program


1. Requirements
----------------
Before running the system, ensure the following:
- Python 3.x is installed on your computer. 
- All project files are located in one folder named:
  SmartLibrary-Group-I
- The folder should include these files:
  demo.py
  operations.py
  security.py
  tests.py
  logs/

2. Open the Project Folder
---------------------------
1. Open Command Prompt or Terminal on your computer.
2. Navigate to the folder that contains your project using the cd command.
   Example:
   cd "C:\\Users\\JOSHUA M K YAFFA\\SmartLibrary-Group-I"

3. Run the Main Program
------------------------
Type this command and press Enter:
   python demo.py

You should see this welcome message:
=====================================
 Welcome to ReadEasy Library System
=====================================
=== Select Role ===
1. Admin
2. Staff
3. Member
Enter your choice (1/2/3):

4. Log In to the System
------------------------
Select a role and log in using the credentials below:

Role       Username    Password
--------------------------------
Admin      admin       admin123
Staff      staff       staff123
Member     (Name only) No password required

Example for Admin:
Enter your choice (1/2/3): 1
Enter username: admin
Enter password: admin123
Welcome, admin! Role: Admin

5. Choose Your Operations
---------------------------
Once logged in, a menu will appear depending on your role.

Admin Menu:
- Add, update, or delete books and members.
- Borrow and return books.
- View system summary.
- Access audit and error logs.

Staff Menu:
- View books and members.
- Borrow or return books.
- View system summary.

Member Menu:
- View available books.
- Borrow or return books.

6. View System Logs
--------------------
All user actions (login, logout, borrowing, errors) are recorded automatically in the logs folder:
   logs/audit_log.txt
   logs/error_log.txt

Example:
[2025-10-16 18:21:04] USER: admin - ACTION: Logged in successfully as admin
[2025-10-16 18:25:10] USER: admin - ACTION: Added new member (ID: M001)

7. Run Automated Tests
-----------------------
To verify that all system functions work correctly:
   python tests.py

Expected output:
   Ran all tests successfully
   OK

This confirms that the program is functioning properly.

8. Logout and Exit
-------------------
To safely log out and end your session:
- Choose option 0 from the menu.

Example:
0
Goodbye, admin. You have been logged out.

The logout event will be saved in the audit_log.txt file with the exact date and time.

9. Common Issues
-----------------
- If Python is not recognized, ensure it’s installed and added to your system PATH.
- Use python3 instead of python on macOS or Linux.
- If logs are missing, make sure the folder 'logs' exists in your project directory.

10. Example Workflow
---------------------
1. Admin logs in using admin/admin123.
2. Admin adds books and members.
3. Staff logs in to help members borrow books.
4. Member logs in by name to view or borrow books.
5. Admin views the audit log to see all activities.



Optional 
1. download python 3.x install it 
2. download PyCharm and install it as well
3. open PyCharm 
4. click on files at the top lefthand conner
5. click open folder and select where you saved the folder 
6. click on open from the small window that appear and click enter on you keyboard 
7. Run the demo.py and follow the instruction from number 3 to 10 above 
