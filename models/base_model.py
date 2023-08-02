#!/usr/bin/python3
"""This module defines the BaseModel class for the HBNB project

The BaseModel class is a base class for all HBNB models It defines common
attributes and methods that are used across all model classes
"""

import uuid
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Integer, Sequence, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage


Base = declarative_base()


class BaseModel:
    """BaseModel class for the HBNB project

    Attributes:
        id (str): The unique identifier for the BaseModel instance
        created_at (datetime): The datetime when the instance is created
        updated_at (datetime): The datetime when the instance is last updated
    """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Return a string representation of the BaseModel instance

        Returns:
            str: A string representation of the instance
        """
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Update the updated_at attribute with the current datetime

        Also, add the instance to the storage and save it to the database
        """
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert the instance into a dictionary format

        Returns:
            dict: A dictionary representation of the instance
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({"__class__": (str(type(self)).split(".")[-1]).split("'")[0]})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            dictionary.pop("_sa_instance_state")
        return dictionary

    def delete(self):
        """Delete the current instance from the storage and save the changes"""
        storage.delete(self)
        storage.save()