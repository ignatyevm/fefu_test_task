from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from api.db.database import Base


class ScientometricDB(Base):
    __tablename__ = "scientometric_db"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    guid = Column(String, nullable=False)
    full_name = Column(String, nullable=False)


class AuthorProfile(Base):
    __tablename__ = "author_profile"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    scientometric_db_id = Column(Integer, ForeignKey('scientometric_db.id'))
    document_count = Column(Integer, default=0)
    citation_count = Column(Integer, default=0)
    h_index = Column(Integer, default=0)
    url = Column(String, nullable=False)
    date = Column(DateTime(timezone=False), server_default=func.now())

    author = relationship(Author)
    scientometric_db = relationship(ScientometricDB)
