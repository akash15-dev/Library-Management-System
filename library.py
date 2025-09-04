from __future__ import annotations
from typing import List, Dict, Optional
from . import storage
from .models import Book, Loan
from .utils import today, add_days, is_overdue, new_loan_id, validate_isbn
from .config import DEFAULT_DUE_DAYS

def list_books(data_dir: str) -> List[Book]:
    return [Book(ISBN=r['ISBN'], Title=r['Title'], Author=r['Author'],
                 CopiesTotal=int(r['CopiesTotal']), CopiesAvailable=int(r['CopiesAvailable']))
            for r in storage.read_csv(data_dir, 'books.csv')]

def add_book(data_dir: str, isbn: str, title: str, author: str, copies: int) -> Book:
    if not validate_isbn(isbn):
        raise ValueError('Invalid ISBN')
    if copies < 0:
        raise ValueError('Negative copies not allowed')
    rows = storage.read_csv(data_dir, 'books.csv')
    for r in rows:
        if r['ISBN'] == isbn:
            # update total/available incrementally
            r['CopiesTotal'] = str(int(r['CopiesTotal']) + copies)
            r['CopiesAvailable'] = str(int(r['CopiesAvailable']) + copies)
            storage.write_csv(data_dir, 'books.csv', rows)
            return Book(ISBN=r['ISBN'], Title=r['Title'], Author=r['Author'],
                        CopiesTotal=int(r['CopiesTotal']), CopiesAvailable=int(r['CopiesAvailable']))
    row = {'ISBN':isbn, 'Title':title, 'Author':author,
           'CopiesTotal':str(copies), 'CopiesAvailable':str(copies)}
    rows.append(row)
    storage.write_csv(data_dir, 'books.csv', rows)
    return Book(ISBN=isbn, Title=title, Author=author, CopiesTotal=copies, CopiesAvailable=copies)

def remove_book(data_dir: str, isbn: str) -> bool:
    rows = storage.read_csv(data_dir, 'books.csv')
    new_rows = [r for r in rows if r['ISBN'] != isbn]
    storage.write_csv(data_dir, 'books.csv', new_rows)
    return len(new_rows) != len(rows)

def search_books(data_dir: str, keyword: str) -> List[Book]:
    kw = keyword.lower()
    return [b for b in list_books(data_dir) if kw in b.Title.lower() or kw in b.Author.lower()]

def _find_book_row(rows: List[Dict[str,str]], isbn: str) -> Optional[Dict[str,str]]:
    for r in rows:
        if r['ISBN'] == isbn:
            return r
    return None

def issue_book(data_dir: str, member_id: str, isbn: str) -> Loan:
    books = storage.read_csv(data_dir, 'books.csv')
    bro = _find_book_row(books, isbn)
    if not bro:
        raise ValueError('Invalid ISBN')
    if int(bro['CopiesAvailable']) <= 0:
        raise ValueError('No copies available')
    loans = storage.read_csv(data_dir, 'loans.csv')
    loan_ids = {l['LoanID'] for l in loans}
    lid = new_loan_id(loan_ids)
    iss = today()
    due = add_days(iss, DEFAULT_DUE_DAYS)
    loan_row = {'LoanID':lid, 'MemberID':member_id, 'ISBN':isbn, 'IssueDate':iss, 'DueDate':due, 'ReturnDate':''}
    loans.append(loan_row)
    storage.write_csv(data_dir, 'loans.csv', loans)
    bro['CopiesAvailable'] = str(int(bro['CopiesAvailable']) - 1)
    storage.write_csv(data_dir, 'books.csv', books)
    return Loan(**loan_row)

def return_book(data_dir: str, loan_id: str) -> bool:
    loans = storage.read_csv(data_dir, 'loans.csv')
    updated = False
    for l in loans:
        if l['LoanID'] == loan_id and l['ReturnDate'] == '':
            l['ReturnDate'] = today()
            updated = True
            # increment book availability
            books = storage.read_csv(data_dir, 'books.csv')
            for b in books:
                if b['ISBN'] == l['ISBN']:
                    b['CopiesAvailable'] = str(int(b['CopiesAvailable']) + 1)
                    break
            storage.write_csv(data_dir, 'books.csv', books)
            break
    if updated:
        storage.write_csv(data_dir, 'loans.csv', loans)
    return updated

def member_loans(data_dir: str, member_id: str) -> List[Loan]:
    return [Loan(**r) for r in storage.read_csv(data_dir, 'loans.csv') if r['MemberID'] == member_id]

def overdue_list(data_dir: str):
    loans = storage.read_csv(data_dir, 'loans.csv')
    return [Loan(**l) for l in loans if l['ReturnDate'] == '' and is_overdue(l['DueDate'])]
