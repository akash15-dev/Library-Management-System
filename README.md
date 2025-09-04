# 📚 Python Library Management System (Console Project) 🚀  

A **menu-driven Library Management System** built in Python.  
This project demonstrates core concepts like authentication, CRUD operations, file-based storage, and role-based access — all using a console interface with `.csv` files as the database.  

---

## 📌 Table of Contents  
- [About the Project](#about-the-project)  
- [Features](#features)  
- [Screenshots](#screenshots)  
- [What I Learned](#what-i-learned)  
- [Contact](#contact)  
- [Project Structure](#project-structure)  

---

## 📖 About the Project  

This project simulates a **real-world library system** where librarians and members have different permissions.  
All data (books, members, loans) is stored in `.csv` files instead of a database.  
Password security is handled using **bcrypt hashing** for safe authentication.  

---

## ✨ Features  

### 👩‍🏫 Librarian  
✅ Add / Remove Books  
✅ Register Members  
✅ Issue Books (auto-sets 14 day due date)  
✅ Return Books (restores availability)  
✅ View Overdue List  

### 👨‍🎓 Member  
✅ Search Catalogue by Title/Author  
✅ Borrow Books (if available)  
✅ View Loan History  

### 🔐 General  
✅ Secure Login with Password Hashing  
✅ Input Validations (duplicate IDs, invalid ISBN, negative copies, etc.)  
✅ Simple CLI Menu Navigation  

---


## 📘 What I Learned  

Building this Library Management System helped me improve my Python & project skills:  

- 🗂️ Modeled **many-to-many relationships** (Members ↔ Loans)  
- 🔐 Used **bcrypt hashing** for authentication  
- 📁 Worked with **CSV files** as a mini-database  
- 🛠️ Practiced CRUD operations in real scenarios  
- 🔄 Implemented **due-date logic & overdue tracking**  
- 🧪 Added simple testing with **pytest**  
- 🎯 Structured a project with multiple modules (auth, storage, business logic)  

---

## 📂 Project Structure  

```bash
library_mgmt/
├── app.py              # Main entry point (console menu)
├── models.py           # Dataclasses for Book, Member, Loan
├── storage.py          # CSV file read/write helpers
├── auth.py             # Login & registration logic
├── library.py          # Business rules (issue/return/search)
├── utils.py            # Helper utilities (e.g., today’s date)
├── data/               # CSV files: books.csv, members.csv, loans.csv
└── tests/              # Pytest cases

## 🙌 Contributing

💡 If you have any suggestions, feel free to open an issue or ping me — I'm happy to collaborate and improve this project together!

---
 
## 📬 Contact

**Akash**  
🔗 [LinkedIn](https://www.linkedin.com)  
📧 akash.sfdc015@gmail.com  

> 🚀 Interested in building cool projects together? Let’s collaborate!

---

🛠️ Built with passion, caffeine ☕, and lots of ❤️  
by Akash 🚀
