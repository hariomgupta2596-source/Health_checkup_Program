"""Authentication utilities.
Provides password hashing and verification using Passlib's bcrypt context.
"""
from passlib.context import CryptContext

# bcrypt with recommended rounds (default 12)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Return a bcrypt hash for the given password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against an existing hash."""
    return pwd_context.verify(plain_password, hashed_password)
