"""Database Model"""
from datetime import datetime
from marshmallow import fields
from extention import db, ma

class URL(db.Model):
    """URL Model"""
    __tablename__ = "shortcode"
    id = db.Column(db.Integer, primary_key=True)
    shortcode = db.Column(db.String(6), unique =True)
    url = db.Column(db.String(150), unique = True)
    createDate = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    lastRedirect =  db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    redirectCount = db.Column(db.Integer)

class URLSchema(ma.SQLAlchemyAutoSchema):
    """URL API Model"""
    class Meta:
        model = URL
        load_instance = True
        sqla_session = db.session

shortcode_schema = URLSchema()
