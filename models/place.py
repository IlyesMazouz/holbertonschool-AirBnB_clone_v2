#!/usr/bin/python3
"""This module defines the Place class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """The Place class, which inherits from BaseModel and Base"""

    __tablename__ = "places"

    city_id = Column(
        String(60), ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    reviews = relationship(
        "Review", backref="place", cascade="all, delete", passive_deletes=True
    )
#!/usr/bin/python3
"""This module defines the Place class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """The Place class, which inherits from BaseModel and Base"""

    __tablename__ = "places"

    city_id = Column(
        String(60), ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    reviews = relationship(
        "Review", backref="place", cascade="all, delete", passive_deletes=True
    )