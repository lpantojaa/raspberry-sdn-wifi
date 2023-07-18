# Import necessary modules for database management and HTTP request handling
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the database table
class MacAddress(Base):
    __tablename__ = 'mac_addresses'
    mac = Column(String, primary_key=True)

# Create engine for SQLite database
engine = create_engine('sqlite:////home/leandro/finalproject/whitelist.db')
Session = sessionmaker(bind=engine)
session = Session()

