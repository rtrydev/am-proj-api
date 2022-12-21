from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.database_provider import DatabaseProvider


class PostgresDatabaseProvider(DatabaseProvider):
    def get_db(self):
        engine = create_engine("postgresql://postgres:mysecretpassword@localhost/amdb")
        factory = sessionmaker(bind=engine)

        return factory()
