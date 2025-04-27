from module import db,login_manager
from flask_login import UserMixin
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    username = db.Column(db.String(),nullable=False,unique=True)
    email = db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    role = db.Column(db.String(),nullable=False,default='staff')

class Staff(db.Model):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    username = db.Column(db.String(),nullable=False,unique=True)
    email = db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    role = db.Column(db.String(),nullable=False,default='staff')

class Products(db.Model):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    name = db.Column(db.String(),nullable=False,unique=True)
    quantity = db.Column(db.Integer(),nullable=False)
    price = db.Column(db.Integer(),nullable=False)
    added_date = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    updated_date = db.Column(db.DateTime,default=lambda: datetime.now(IST),onupdate=lambda: datetime.now(IST))

class Reports(db.Model):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    name = db.Column(db.String(),nullable=False)
    quantity = db.Column(db.Integer(),nullable=False)
    price = db.Column(db.Integer(),nullable=False)
    time = db.Column(db.DateTime, default=lambda: datetime.now(IST))

class Notification(db.Model):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    content = db.Column(db.String(),nullable=False)
    time = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    is_read = db.Column(db.Boolean, default=False)