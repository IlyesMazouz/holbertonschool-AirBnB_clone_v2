#!/usr/bin/python3
"""This module defines the Review class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """The Review class, which inherits from BaseModel and Base"""

    __tablename__ = "reviews"

    text = Column(String(1024), nullable=False)
    place_id = Column(
        String(60), ForeignKey("places.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
