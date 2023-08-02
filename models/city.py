#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if HBNB_TYPE_STORAGE == 'db':
        places = relationship("Place", backref="cities", cascade="all, delete")
    else:
        @property
        def places(self):
            """ Returns the list of Place instances with city_id equal to the current City.id """
            from models import storage
            from models.place import Place
            places_list = []
            for place in storage.all(Place).values():
                if place.city_id == self.id:
                    places_list.append(place)
            return places_list
