from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    owner = db.Column(db.String(50), nullable=False)

class AdvertSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Advert
        include_fk = True