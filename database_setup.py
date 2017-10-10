###### Start of Congfiguration code put at the beginning #########
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

####### End of Configuration code put at the beginning ###########

class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(String(80), nullable = False)
    id = Column(Integer,primary_key = True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80),nullable = False)
    id = Column(Integer, primary_key=True)
    course = Column(String(80))
    description = Column(String(80))
    price = Column(String(80))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name'  :   self.name,
            'description'   :   self.description,
            'id'    :   self.id,
            'price' :   self.price,
            'course'    :   self.course
        }

######### insert at the end of the file ##########
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)