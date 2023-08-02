#!/usr/bin/python3
"""This module defines the DBStorage class for HBNB project

It provides a database storage implementation using SQLAlchemy to store and
manage data for the hbnb project models
"""

from sqlalchemy import Column, Integer, Sequence, String, DateTime
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DBStorage class for HBNB project

    Attributes:
        __engine (Engine): The SQLAlchemy engine
        __session (Session): The current session for the database
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new database storage

        Create the engine to connect to the MySQL database using SQLAlchemy
        If the environment is set to 'test', drop all tables
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects from the database

        Return a dictionary containing all objects of a specific class or
        all classes if cls is None

        Args:
            cls (class, optional): The class to query objects from

        Returns:
            dict: A dictionary containing the queried objects with their
                  unique key (class_name.id)
        """
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        return objects

    def new(self, obj):
        """Add an object to the database session

        Args:
            obj (BaseModel): The object to add

        Returns:
            None
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes in the database session

        Returns:
            None
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database session

        Args:
            obj (BaseModel, optional): The object to delete

        Returns:
            None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload database tables and create a new database session

        Returns:
            None
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Close the database session

        Returns:
            None
        """
        self.__session.close()

