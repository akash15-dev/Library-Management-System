from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    ISBN: str
    Title: str
    Author: str
    CopiesTotal: int
    CopiesAvailable: int

@dataclass
class Member:
    MemberID: str
    Name: str
    PasswordHash: str
    Email: str
    JoinDate: str  # YYYY-MM-DD

@dataclass
class Loan:
    LoanID: str
    MemberID: str
    ISBN: str
    IssueDate: str  # YYYY-MM-DD
    DueDate: str    # YYYY-MM-DD
    ReturnDate: str # YYYY-MM-DD or ''

@dataclass
class User:
    Username: str
    PasswordHash: str
    Role: str
    Name: str
    Email: str
