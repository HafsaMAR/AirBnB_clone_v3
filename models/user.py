#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        hashed_password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        self.password = ''

    
    @property
    def password_hash(self):
        """Getter for the password hash"""
        return self.__password_hash
    
    @password_hash.setter
    def password_hash(self, value):
        """Setter for the password hash"""
        if value:
            self.__password_hash = hashlib.md5(value.encode()).hexdigest()
                
    def to_dict(self, **kwargs):
        """Return a dictionary representation of the user instance"""
        if models.storage_t == 'db' or 'password' in kwargs:
            return super().to_dict(**kwargs)
        else:
            dict_copy = super().to_dict(**kwargs)
            dict_copy.pop('password', None)
            dict_copy['hashed_password'] = self.password_hash
        return dict_copy
