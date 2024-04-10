"""Database Model"""
from datetime import datetime
from extention import db, ma

class URL(db.Model):
    """URL Model"""
    __tablename__ = "shortcode"
    id_ = db.Column(db.Integer, primary_key=True)
    shortcode = db.Column(db.String(6), unique =True)
    url = db.Column(db.String(150), unique = True)
    shortened_url= db.Column(db.String(100), unique = True)
    createDate = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    lastRedirect = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    redirectCount = db.Column(db.Integer)

class URLSchema(ma.SQLAlchemyAutoSchema):
    """URL API Model"""
    class Meta:
        """Configuring SQLAlchemy behavior for the URL model"""
        model = URL
        load_instance = True
        sqla_session = db.session
