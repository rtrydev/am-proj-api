import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.database_provider import DatabaseProvider


class PostgresDatabaseProvider(DatabaseProvider):
    def get_db(self):
        connection_string = os.environ.get("PERSISTENT_DB_CONNECTION_STRING")

        engine = create_engine(connection_string)
        factory = sessionmaker(bind=engine)

        return factory()
