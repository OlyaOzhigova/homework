from sqlalchemy import Column, Integer, String, DateTime, select
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields

Base = declarative_base()

class Advert(Base):
    __tablename__ = 'adverts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False)
    owner = Column(String(50), nullable=False)
    
    select = select

class AdvertSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    owner = fields.Str(required=True)