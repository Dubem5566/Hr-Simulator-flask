from .database import db
from datetime import datetime

class Clockin(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    Clock_in_time = db.Column(db.DateTime, default = datetime.utcnow)