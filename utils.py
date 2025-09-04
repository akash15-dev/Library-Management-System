from __future__ import annotations
import datetime as dt
import re, uuid

DATE_FMT = "%Y-%m-%d"

def today() -> str:
    return dt.date.today().strftime(DATE_FMT)

def add_days(date_str: str, days: int) -> str:
    d = dt.datetime.strptime(date_str, DATE_FMT).date()
    d2 = d + dt.timedelta(days=days)
    return d2.strftime(DATE_FMT)

def is_overdue(due_date: str, return_date: str='') -> bool:
    if return_date:
        return False
    return dt.datetime.strptime(due_date, DATE_FMT).date() < dt.date.today()

def new_member_id(existing_ids: set[str]) -> str:
    base = 1000
    while str(base) in existing_ids:
        base += 1
    return str(base)

def new_loan_id(existing_ids: set[str]) -> str:
    # simple numeric increment, fallback to uuid
    base = 1
    while str(base) in existing_ids:
        base += 1
        if base > 10_000_000:
            return uuid.uuid4().hex[:8]
    return str(base)

def validate_isbn(isbn: str) -> bool:
    return bool(re.fullmatch(r"[0-9Xx-]+", isbn))
