import os
from sqlalchemy import Column, DateTime, String, Boolean, ARRAY
import sqlalchemy_jsonfield
from sqlalchemy.ext.declarative import declarative_base

# get db path
if 'RSVP_DB_PATH' in os.environ:
    RSVP_DB_PATH = os.environ['RSVP_DB_PATH']
else:
    RSVP_DB_PATH = '/tmp/rsvp.db'

Base = declarative_base()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class invitation(Base):
    __tablename__ = 'rsvp'
    id = Column(String, primary_key=True, )
    guest = Column(sqlalchemy_jsonfield.JSONField(
            enforce_string=False,
            enforce_unicode=False
        ),
        nullable=False
    )
    email = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    rsvped = Column(Boolean)
    table = Column(Boolean)
    date = Column(DateTime(), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'guest': self.guest,
            'email': self.email,
            'comment': self.comment,
            'phone': self.phone,
            'rsvped': self.rsvped,
            'table': self.table,
            'date': dump_datetime(self.date)
        }

from sqlalchemy import create_engine

engine = create_engine('sqlite:///'+RSVP_DB_PATH)

from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)