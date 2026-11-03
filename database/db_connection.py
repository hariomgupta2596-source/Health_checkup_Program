import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database file placed in project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'health_checkup.db')

engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Yield a SQLAlchemy session.
    Usage:
        from database.db_connection import get_db
        with get_db() as db:
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
