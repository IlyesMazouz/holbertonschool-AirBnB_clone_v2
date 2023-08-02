#!/usr/bin/python3
"""This module defines the BaseModel class for the HBNB project

The BaseModel class serves as the base for all other models in the HBNB
project It defines common attributes and methods that other models will
inherit
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
        id (str): The unique identifier for the model instance
        created_at (datetime): The datetime when the instance was created
        updated_at (datetime): The datetime when the instance was last updated
    """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new model instance

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Attributes:
            id (str): The unique identifier for the model instance
            created_at (datetime): The datetime when the instance was created
            updated_at (datetime): The datetime when the instance was last updated

        Returns:
            None
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
        """Return a string representation of the instance

        Returns:
            str: The string representation of the instance
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Update updated_at with current time and save the instance to storage

        Returns:
            None
        """
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert the instance into a dictionary format

        Returns:
            dict: The dictionary representation of the instance
        """
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                           (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            dictionary.pop("_sa_instance_state")
        return dictionary

    def delete(self):
        """Delete the current instance and save the change to storage

        Returns:
            None
        """
        storage.delete(self)
        storage.save()
