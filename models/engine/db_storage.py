#!/usr/bin/python3
"""This module defines the DBStorage engine"""

from os import getenv
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class manages the storage using SQLAlchemy with MySQL"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST, HBNB_MYSQL_DB), pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        all_dict = {}
        for itr in models.classes.keys():
            if cls is None or cls == models.classes[itr] or cls == itr:
                objs = self.__session.query(models.classes[itr]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    all_dict[key] = obj
        return all_dict

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """Dispose of the current session"""
        self.__session.remove()
