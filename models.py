from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()
 
class itemModel(db.Model):
    __tablename__ = "table"

    itemID = db.Column(db.Integer(), unique = True, primary_key = True)
    quantity = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), primary_key = True)
    dateAdded = db.Column(db.String(), primary_key = True)
    category = db.Column(db.String(), primary_key = True)
    location = db.Column(db.String(), primary_key = True)
    deleted = db.Column(db.Boolean(), primary_key = True)
    deletionComment = db.Column(db.String(), primary_key = True)
    
 
    def __init__(self, name, category, location, quantity):
        self.itemID = 1
        self.name = name
        self.dateAdded = date.today().strftime("%m/%d/%y")
        self.category = category
        self.location = location
        self.deleted = False
        self.deletionComment = ''
 
    def __repr__(self):
        return f"{self.name}:{self.itemID}"