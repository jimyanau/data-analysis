# use this module to handle path across different operation systems
from os import path

# descrip object relational mapping
from sqlalchemy import (create_engine,
						Column,
						String,
						Integer,
						Boolean,
						Table,
						ForeignKey)

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

database_filename = 'twitter.sqlite3'

directory = path.abspath(path.dirname(__file__))
database_filepath = path.join(directory, database_filename)

engine_url = 'sqlite:///{}'.format(database_filepath)

engine = create_engine(engine_url)