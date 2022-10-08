from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import close_all_sessions

from api.config import get_database_url

Base = declarative_base()


class Database:
    def __init__(self, database_url: str = Depends(get_database_url)):
        self.__engine = create_engine(database_url)
        self.__session_factory = sessionmaker(bind=self.__engine)

    def get_session(self):
        return self.__session_factory()

    def create_db(self):
        Base.metadata.create_all(self.__engine)

    def close(self):
        close_all_sessions()
