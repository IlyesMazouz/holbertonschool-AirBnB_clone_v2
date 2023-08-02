#!/usr/bin/python3
"""This module defines the DBStorage class for the HBNB project

The DBStorage class manages the storage of HBNB models in the database
It provides methods for querying, adding, saving, and deleting objects
"""

from sqlalchemy import create_engine
from os import getenv
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.base_model import BaseModel, Base
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """DBStorage class for the HBNB project

    Attributes:
        __engine (Engine): The database engine for SQLAlchemy
        __session (Session): The current database session
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new database storage and create the engine."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current database session for objects of the given class

        If cls is None, it queries all types of objects
        Returns:
            dict: A dictionary of queried classes in the format
            <class name>.<obj id> = obj
        """
        if cls is None:
            objs = self.__session.query(State, City, User,
                                        Review, Place, Amenity).all()
        else:
            objs = self.__session.query(cls.__class__.__name__)
        resu = {}
        for obj in objs:
            resu[obj.__class__.__name__ + "." + obj.id] = obj
        return resu

    def new(self, obj):
        """Add obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database"""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)

        self.__session = Session()
        