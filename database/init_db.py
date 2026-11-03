"""Initialize the SQLite database for Health Checkup Program.
Run this script once (or any time you need to reset the schema):

    python -m database.init_db
"""
from .db_setup import create_all

if __name__ == "__main__":
    create_all()
