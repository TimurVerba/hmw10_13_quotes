import os
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine, Column, String, ARRAY, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
postgres_uri = os.getenv("POSTGRES_URI")


mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['goit']
authors_collection = mongo_db['authors']
quotes_collection = mongo_db['quotes']


postgres_engine = create_engine(postgres_uri)
Base = declarative_base()



class Author(Base):
    __tablename__ = 'quotes_author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String, nullable=False)
    born_date = Column(String)
    born_location = Column(String)
    description = Column(String)


class Quote(Base):
    __tablename__ = 'quotes_quote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tags = Column(ARRAY(String))
    author_id = Column(Integer, ForeignKey('quotes_author.id'))
    quote = Column(String, nullable=False)



Base.metadata.create_all(postgres_engine)


Session = sessionmaker(bind=postgres_engine)
session = Session()


def migrate_data():
    mongo_author_id_mapping = {}
    for author_doc in authors_collection.find():
        existing_author = session.query(Author).filter_by(fullname=author_doc['fullname']).first()

        if not existing_author:
            author = Author(
                fullname=author_doc['fullname'],
                born_date=author_doc.get('born_date', ''),
                born_location=author_doc.get('born_location', ''),
                description=author_doc.get('description', '')
            )
            session.add(author)
            session.commit()
            mongo_author_id_mapping[str(author_doc['_id'])] = author.id


    for quote_doc in quotes_collection.find():
        existing_quote = session.query(Quote).filter_by(quote=quote_doc['quote']).first()

        if not existing_quote:
            quote = Quote(
                tags=quote_doc['tags'],
                author_id=mongo_author_id_mapping.get(str(quote_doc['author']), None),
                quote=quote_doc['quote']
            )
            session.add(quote)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()

    session.close()

if __name__ == "__main__":
    migrate_data()
