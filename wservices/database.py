import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.ext.declarative import declarative_base

engine = None
db_session = scoped_session(lambda: create_session(autocommit=False, bind=engine))

Base = declarative_base()
# Base.query = db_session.query_property()


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine


def init_db():
    from models import User
    Base.metadata.create_all(bind=engine)

    # creating a default user for login
    default_user = db_session.query(User).first()
    if not default_user:
        if os.environ.get("DEFAULT_APP_USER") and len(os.environ.get("DEFAULT_APP_USER")) > 2 \
                and os.environ.get("DEFAULT_APP_PASSWORD") and len(os.environ.get("DEFAULT_APP_PASSWORD")) > 2:
            new_user = User(
                name="FulFil IO",
                user=os.environ.get("DEFAULT_APP_USER"),
                password=os.environ.get("DEFAULT_APP_PASSWORD")
            )
            db_session.add(new_user)
            try:
                db_session.commit()
            except Exception as e:
                print("Error creating default user for app.")

