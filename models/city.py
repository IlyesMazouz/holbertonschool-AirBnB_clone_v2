#!/usr/bin/python3
"""This module defines the City class for the HBNB project

The City class represents a city and contains attributes related to a city
such as its name, state ID, and the relationship with the Place class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """City class for the HBNB project

    Attributes:
        __tablename__ (str): The table name for the City class
        name (str): The name of the city
        state_id (str): The state ID to which the city belongs
        places (relationship): The relationship with the Place class, representing
            all places associated with this city
    """

    __tablename__ = "cities"

    name = Column(String(128), nullable=False)
    state_id = Column(
        String(60), ForeignKey("states.id", ondelete="CASCADE"), nullable=False
    )
    places = relationship(
        "Place", backref="cities", cascade="all, delete", passive_deletes=True
    )
