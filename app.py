from __future__ import annotations
import argparse
from typing import Optional
import auth
import library
# auth.py (fixed)
import storage
from models import Member, User
from utils import today



def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s

def librarian_menu(data_dir: str, user: User):
    while True:
        print("""\n=== Librarian Dashboard ===
1. Add Book
2. Remove Book
3. Register Member
4. Issue Book
5. Return Book
6. Overdue List
7. Logout""")
        choice = input("> ").strip()
        try:
            if choice == '1':
                isbn = input_nonempty('ISBN: ')
                title = input_nonempty('Title: ')
                author = input_nonempty('Author: ')
                copies = int(input_nonempty('Copies: '))
                b = library.add_book(data_dir, isbn, title, author, copies)
                print(f"✔ Added/updated {b.Title} ({b.ISBN}). Available: {b.CopiesAvailable}")
            elif choice == '2':
                isbn = input_nonempty('ISBN to remove: ')
                ok = library.remove_book(data_dir, isbn)
                print('✔ Removed' if ok else '✖ Not found')
            elif choice == '3':
                name = input_nonempty('Member name: ')
                email = input_nonempty('Email: ')
                pw = input_nonempty('Temp password: ')
                m = auth.register_member(data_dir, name, email, pw)
                print(f"✔ Registered member {m.Name} with ID {m.MemberID}")
            elif choice == '4':
                isbn = input_nonempty('ISBN to issue: ')
                mid = input_nonempty('Member ID: ')
                loan = library.issue_book(data_dir, mid, isbn)
                print(f"✔ Book issued. Due on {loan.DueDate} (LoanID {loan.LoanID}).")
            elif choice == '5':
                lid = input_nonempty('LoanID to return: ')
                ok = library.return_book(data_dir, lid)
                print('✔ Returned' if ok else '✖ Loan not found or already returned')
            elif choice == '6':
                ol = library.overdue_list(data_dir)
                if not ol:
                    print('No overdue loans.')
                else:
                    print('Overdue Loans:')
                    for l in ol:
                        print(f"Loan {l.LoanID} | Member {l.MemberID} | ISBN {l.ISBN} | Due {l.DueDate}")
            elif choice == '7':
                print('Logged out.')
                break
            else:
                print('Invalid option.')
        except Exception as e:
            print(f"Error: {e}")

def member_menu(data_dir: str, member: Member):
    while True:
        print("""\n=== Member Menu ===
1. Search Catalogue
2. Borrow Book
3. My Loans
4. Logout""")
        ch = input("> ").strip()
        try:
            if ch == '1':
                kw = input_nonempty('Keyword (title/author): ')
                res = library.search_books(data_dir, kw)
                if not res: print('No matches.')
                for b in res:
                    print(f"{b.Title} by {b.Author} | {b.ISBN} | Avail {b.CopiesAvailable}/{b.CopiesTotal}")
            elif ch == '2':
                isbn = input_nonempty('ISBN to borrow: ')
                loan = library.issue_book(data_dir, member.MemberID, isbn)
                print(f"✔ Borrowed. Due {loan.DueDate}. LoanID {loan.LoanID}")
            elif ch == '3':
                loans = library.member_loans(data_dir, member.MemberID)
                if not loans:
                    print('No loans.')
                else:
                    for l in loans:
                        status = 'Returned' if l.ReturnDate else 'On loan'
                        print(f"Loan {l.LoanID} | {status} | Issue {l.IssueDate} | Due {l.DueDate} | Return {l.ReturnDate}")
            elif ch == '4':
                print('Logged out.')
                break
            else:
                print('Invalid option.')
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Library Management System (CSV)')
    parser.add_argument('--data-dir', default='./data', help='Directory for CSV files')
    args = parser.parse_args()

    storage.ensure_files(args.data_dir)
    auth.ensure_admin_user(args.data_dir)

    while True:
        print("""\n=== Welcome ===
1. Login as Librarian
2. Login as Member
3. Exit""")
        s = input("> ").strip()
        if s == '1':
            u = input_nonempty('Username: ')
            p = input_nonempty('Password: ')
            user = auth.login_librarian(args.data_dir, u, p)
            if user: librarian_menu(args.data_dir, user)
            else: print('✖ Invalid credentials')
        elif s == '2':
            mid = input_nonempty('Member ID: ')
            pw = input_nonempty('Password: ')
            m = auth.login_member(args.data_dir, mid, pw)
            if m: member_menu(args.data_dir, m)
            else: print('✖ Invalid credentials')
        elif s == '3':
            print('Bye!')
            break
        else:
            print('Invalid option.')

if __name__ == '__main__':
    main()
