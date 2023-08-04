#!/usr/bin/python3
"""This module defines the Amenity class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """The Amenity class, which inherits from BaseModel and Base"""

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
