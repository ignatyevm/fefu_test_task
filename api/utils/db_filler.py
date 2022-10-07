from api.db.database import Database
from api.models.models import Author, AuthorProfile, ScientometricDB


def fill(database: Database, authors, scientometric_databases, profiles):
    database.create_db()

    session = database.get_session()
    for guid, full_name in authors:
        session.add(Author(guid=guid, full_name=full_name))
        session.commit()

    for scientometric_database in scientometric_databases:
        session.add(ScientometricDB(name=scientometric_database))
        session.commit()

    for guid, scientometric_database, document_count, citation_count, h_index, url in profiles:
        author = session.query(Author).where(Author.guid == guid).first()
        scientometric_database = session.query(ScientometricDB).where(
            ScientometricDB.name == scientometric_database).first()
        session.add(AuthorProfile(author=author, scientometric_db=scientometric_database, document_count=document_count,
                                  citation_count=citation_count, h_index=h_index, url=url))
        session.commit()

    session.close()


def refill(database: Database, authors, scientometric_databases, profiles):
    session = database.get_session()
    session.execute("DROP TABLE IF EXISTS author, scientometric_db, author_profile;")
    session.commit()
    session.close()
    fill(database, authors, scientometric_databases, profiles)
