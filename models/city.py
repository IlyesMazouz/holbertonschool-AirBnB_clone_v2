#!/usr/bin/python3
"""This module defines the City class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """The City class, which inherits from BaseModel and Base"""

    __tablename__ = "cities"

    name = Column(String(128), nullable=False)

    places = relationship(
        "Place", backref="cities", cascade="all, delete", passive_deletes=True
    )
