from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def configure_db(app):
    db = SQLAlchemy(app)
    Base.metadata.create_all(db.engine)

    return db
