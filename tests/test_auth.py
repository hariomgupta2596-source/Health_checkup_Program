import pytest
import os
from datetime import datetime

from authentication import get_password_hash, verify_password
from database.db_connection import engine
from database.db_setup import users, checkups, conditions, create_all

# Helper to clean up a user by username
def _delete_user(username: str):
    with engine.begin() as conn:
        conn.execute(users.delete().where(users.c.username == username))

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Ensure tables exist
    create_all()
    # Run test
    yield
    # Cleanup any test users (username starts with "test_user_")
    with engine.begin() as conn:
        conn.execute(users.delete().where(users.c.username.like("test_user_%")))
        # Also delete any checkups for those users
        conn.execute(checkups.delete().where(checkups.c.user_id.in_(
            conn.execute(users.select().with_only_columns([users.c.id])).fetchall()
        ))
        # Conditions will be cascade‑deleted via foreign key

def test_register_and_login_success():
    username = f"test_user_{datetime.utcnow().timestamp()}"
    email = f"{username}@example.com"
    raw_password = "StrongPass123!"
    pwd_hash = get_password_hash(raw_password)

    # Insert user
    with engine.begin() as conn:
        conn.execute(users.insert().values(username=username, email=email, password_hash=pwd_hash, created_at=datetime.utcnow()))

    # Retrieve and verify password
    with engine.connect() as conn:
        row = conn.execute(users.select().where(users.c.username == username)).fetchone()
        assert row is not None
        assert row["email"] == email
        assert verify_password(raw_password, row["password_hash"]) is True
        # Wrong password should fail
        assert verify_password("WrongPass", row["password_hash"]) is False

def test_register_duplicate_username_fails():
    username = "test_user_duplicate"
    email1 = "dup1@example.com"
    email2 = "dup2@example.com"
    pwd_hash = get_password_hash("pwd")
    # First insert should succeed
    with engine.begin() as conn:
        conn.execute(users.insert().values(username=username, email=email1, password_hash=pwd_hash, created_at=datetime.utcnow()))
    # Second insert with same username should raise an IntegrityError
    with pytest.raises(Exception):
        with engine.begin() as conn:
            conn.execute(users.insert().values(username=username, email=email2, password_hash=pwd_hash, created_at=datetime.utcnow()))
