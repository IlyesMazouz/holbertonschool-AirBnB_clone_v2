#!/usr/bin/python3
"""This module defines the DBStorage engine for HBNB"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City

class DBStorage:
    """This class manages storage of hbnb models in a database using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and links it to the MySQL database"""
        user = os.environ.get('HBNB_MYSQL_USER')
        pwd = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        db = os.environ.get('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries all objects of a given class from the database"""
        objects = {}
        if cls:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            classes = [State, City]  
            for cls in classes:
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Adds a new object to the database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and creates the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        self.__session = scoped_session(session_factory)
