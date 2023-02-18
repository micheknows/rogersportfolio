from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PortfolioItem(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    short_desc = Column(Text)
    long_desc = Column(Text)
    image = Column(String(100))
    demo_link = Column(String(100))
    github_link = Column(String(100))



class PortfolioItemDB:
    def __init__(self, database_uri='mysql+pymysql://micheknows:ph0nics3@localhost/portfolio'):
        self.engine = create_engine(database_uri)
        self.Session = sessionmaker(bind=self.engine)

    def create(self, item):
        session = self.Session()
        session.add(item)
        session.commit()
        session.close()

    def read(self, id):
        session = self.Session()
        item = session.query(PortfolioItem).filter_by(id=id).first()
        session.close()
        return item

    def read_all(self):
        session = self.Session()
        items = session.query(PortfolioItem).all()
        session.close()
        return items

    def update(self, item):
        session = self.Session()
        session.merge(item)
        session.commit()
        session.close()

    def delete(self, id):
        session = self.Session()
        item = session.query(PortfolioItem).filter_by(id=id).first()
        session.delete(item)
        session.commit()
        session.close()

