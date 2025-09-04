from __future__ import annotations
from typing import Optional, Dict
import bcrypt
from . import storage
from .models import Member, User
from .utils import today
from .config import BCRYPT_ROUNDS

def _hash_password(pw: str) -> str:
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(pw.encode('utf-8'), salt).decode('utf-8')

def _check_password(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def register_member(data_dir: str, name: str, email: str, password: str) -> Member:
    members = storage.read_csv(data_dir, 'members.csv')
    ids = {m['MemberID'] for m in members}
    from .utils import new_member_id
    mid = new_member_id(ids)
    mh = _hash_password(password)
    mrow = {
        'MemberID': mid,
        'Name': name,
        'PasswordHash': mh,
        'Email': email,
        'JoinDate': today(),
    }
    members.append(mrow)
    storage.write_csv(data_dir, 'members.csv', members)
    return Member(**mrow)

def ensure_admin_user(data_dir: str):
    users = storage.read_csv(data_dir, 'users.csv')
    if not users:
        # default admin/admin123
        ph = _hash_password('admin123')
        users.append({
            'Username':'admin','PasswordHash':ph,'Role':'Librarian','Name':'Head Librarian','Email':'admin@example.com'
        })
        storage.write_csv(data_dir, 'users.csv', users)

def login_librarian(data_dir: str, username: str, password: str) -> Optional[User]:
    ensure_admin_user(data_dir)
    users = storage.read_csv(data_dir, 'users.csv')
    for u in users:
        if u['Username'] == username and u['Role'] == 'Librarian' and _check_password(password, u['PasswordHash']):
            return User(**u)
    return None

def login_member(data_dir: str, member_id: str, password: str) -> Optional[Member]:
    members = storage.read_csv(data_dir, 'members.csv')
    for m in members:
        if m['MemberID'] == member_id:
            if _check_password(password, m['PasswordHash']):
                return Member(**m)
    return None
