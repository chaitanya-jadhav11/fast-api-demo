from sqlalchemy import Column, Integer, String, Float

from core.database import Base

""" Equal to below Java code
 @Entity
 @Table(name = "products")
 public class Product
    id = Column(Integer, primary_key=True)
 
"""
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

