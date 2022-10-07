from typing import List

from fastapi import Depends
from sqlalchemy import asc, column, desc, func
from sqlalchemy.sql.elements import and_

from api.db.database import Database
from api.models.models import Author, AuthorProfile, ScientometricDB


class ProfileRepository:
    def __init__(self, database: Database = Depends()):
        self.__database = database
        self.__current_session = database.get_session()

    def get_current_session(self):
        return self.__current_session

    def begin_transaction(self):
        self.__current_session.begin()

    def commit_transaction(self):
        self.__current_session.commit()

    def find_profiles(self, scientometric_database: str, limit: int, offset: int,
                      order_field: str, order_dir: str) -> List[AuthorProfile]:
        order_direction = asc if order_dir == "asc" else desc
        session = self.get_current_session()
        author_profiles = session.query(AuthorProfile) \
            .with_entities(Author.full_name, AuthorProfile.h_index, AuthorProfile.url) \
            .join(Author, AuthorProfile.author) \
            .join(ScientometricDB, AuthorProfile.scientometric_db) \
            .where(ScientometricDB.name == scientometric_database) \
            .order_by(order_direction(column(order_field))) \
            .limit(limit).offset(offset).all()
        return author_profiles

    def find_profile(self, guid: str, scientometric_database: str, optional_fields: List[str] = []) -> AuthorProfile:
        optional_fields = [column(field) for field in optional_fields]
        session = self.get_current_session()
        author_profile = session.query(AuthorProfile) \
            .with_entities(Author.full_name, AuthorProfile.h_index, AuthorProfile.url, *optional_fields) \
            .join(Author, AuthorProfile.author) \
            .join(ScientometricDB, AuthorProfile.scientometric_db) \
            .where(and_(Author.guid == guid, ScientometricDB.name == scientometric_database)).first()
        return author_profile

    def find_author_by_guid(self, guid: str) -> Author:
        session = self.get_current_session()
        author = session.query(Author).where(Author.guid == guid).first()
        return author

    def find_scientometric_db_by_name(self, name: str) -> ScientometricDB:
        session = self.get_current_session()
        scientometric_db = session.query(ScientometricDB).where(ScientometricDB.name == name).first()
        return scientometric_db

    def create_author(self, author: Author) -> Author:
        session = self.get_current_session()
        session.add(author)
        return author

    def create_profile(self, profile: AuthorProfile):
        session = self.get_current_session()
        session.add(profile)
        return profile

    def get_statistics(self):
        session = self.get_current_session()
        statistics = session.query(ScientometricDB) \
            .with_entities(ScientometricDB.name.label("scientometric_db"),
                           func.sum(AuthorProfile.document_count).label("total_document_count"),
                           func.sum(AuthorProfile.citation_count).label("total_citation_count"),
                           func.avg(AuthorProfile.h_index).label("average_h_index")) \
            .join(Author, AuthorProfile.author) \
            .join(ScientometricDB, AuthorProfile.scientometric_db) \
            .group_by(ScientometricDB.name).all()
        return statistics
