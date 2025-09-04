from __future__ import annotations
import csv, os
from typing import List, Dict

HEADERS = {
    'books.csv': ['ISBN','Title','Author','CopiesTotal','CopiesAvailable'],
    'members.csv': ['MemberID','Name','PasswordHash','Email','JoinDate'],
    'loans.csv': ['LoanID','MemberID','ISBN','IssueDate','DueDate','ReturnDate'],
    'users.csv': ['Username','PasswordHash','Role','Name','Email'],
}

def ensure_files(data_dir: str):
    os.makedirs(data_dir, exist_ok=True)
    for fname, headers in HEADERS.items():
        path = os.path.join(data_dir, fname)
        if not os.path.exists(path):
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

def read_csv(data_dir: str, name: str) -> List[Dict[str,str]]:
    path = os.path.join(data_dir, name)
    if not os.path.exists(path):
        ensure_files(data_dir)
    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(data_dir: str, name: str, rows: List[Dict[str,str]]):
    path = os.path.join(data_dir, name)
    headers = HEADERS[name]
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
