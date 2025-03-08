import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session, declarative_base

load_dotenv()


Base = declarative_base()
engine = create_engine(os.getenv("RELATIONAL_DATABASE_URI"))


def get_session():
    """Get a new session."""
    session = Session(engine, autocommit=False, autoflush=False)
    try:
        yield session
    except StatementError:
        session.rollback()
        raise
    finally:
        session.close()
