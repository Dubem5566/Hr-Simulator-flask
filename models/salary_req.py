from .database import db

class Sal_req(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    I_D = db.Column(db.String(50))
    Name = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    Request = db.Column(db.String(100))