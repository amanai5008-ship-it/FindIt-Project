FindIt – Lost and Found Portal

About the Project

FindIt is a simple Lost and Found Portal made using Python. It helps users report lost and found items and manage their details in one place.

The main purpose of this project is to make it easier to find lost items and keep records of found items.

Technologies Used

- Python: Main programming language.
- Tkinter: Used to create the graphical user interface (GUI).
- SQLite: Used to store item details in a database.
- VS Code: Used to write and run the code.

Features

1. Dashboard: Shows the total number of lost items, found items, and reports.
2. Report Lost Item: Allows users to enter details of lost items.
3. Report Found Item: Allows users to enter details of found items.
4. Search Items: Helps users search for items by name, category, or location.
5. View Records: Displays all saved item details in a table.
6. Delete Record: Allows users to delete a selected record.

Database

This project uses an SQLite database named "findit.db".

All item details are stored locally in a table named "items".

The database stores:

- Item ID
- Item Type (Lost or Found)
- Item Name
- Category
- Location
- Date
- Description

How to Run the Project

Step 1: Install Python

Download and install Python from:
https://www.python.org/downloads/

Step 2: Download the Project

Clone this repository or download the project files.

Step 3: Open the Project

Open the project folder in VS Code.

Step 4: Run the Application

Open the terminal and type:

py findit.py

Or run the "findit.py" file using the Run Python File option in VS Code.

Project Structure

FindIt_Project/
│
├── findit.py
├── findit.db
└── README.md

Note: The database file may be created automatically when the application runs for the first time.

Advantages

- Easy to use.
- Saves item details in a database.
- Makes searching for items easier.
- Keeps lost and found records organized.
- Data remains saved after closing the application.

Future Improvements

- Add user login and registration.
- Add image upload for items.
- Add online database support.
- Add notifications when a matching item is found.

Developed By

Name: AMAN MADNANI
Student in SRM University
---

Conclusion

FindIt is a simple project that helps manage lost and found items using Python, Tkinter, and SQLite. It provides an easy way to add, search, view, and delete item records.
