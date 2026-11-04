import pytest
from datetime import datetime

from authentication import get_password_hash, verify_password
from database.db_connection import engine
from database.db_setup import users, checkups, conditions, create_all


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    create_all()
    yield
    with engine.begin() as conn:
        conn.execute(users.delete().where(users.c.username.like("test_user_%")))


def test_password_hash_and_verify():
    raw_password = "StrongPass123!"
    pwd_hash = get_password_hash(raw_password)
    assert verify_password(raw_password, pwd_hash) is True
    assert verify_password("WrongPassword", pwd_hash) is False


def test_register_and_login_success():
    username = f"test_user_{datetime.utcnow().timestamp()}"
    email = f"{username}@example.com"
    raw_password = "StrongPass123!"
    pwd_hash = get_password_hash(raw_password)

    with engine.begin() as conn:
        conn.execute(
            users.insert().values(
                username=username,
                email=email,
                password_hash=pwd_hash,
                created_at=datetime.utcnow(),
            )
        )

    with engine.connect() as conn:
        row = conn.execute(users.select().where(users.c.username == username)).mappings().fetchone()
        assert row is not None
        assert row["email"] == email
        assert verify_password(raw_password, row["password_hash"]) is True


def test_register_duplicate_username_fails():
    username = "test_user_duplicate"
    email1 = "dup1@example.com"
    email2 = "dup2@example.com"
    pwd_hash = get_password_hash("pwd")

    with engine.begin() as conn:
        conn.execute(
            users.insert().values(
                username=username,
                email=email1,
                password_hash=pwd_hash,
                created_at=datetime.utcnow(),
            )
        )

    with pytest.raises(Exception):
        with engine.begin() as conn:
            conn.execute(
                users.insert().values(
                    username=username,
                    email=email2,
                    password_hash=pwd_hash,
                    created_at=datetime.utcnow(),
                )
            )
