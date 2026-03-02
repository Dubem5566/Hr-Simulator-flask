from .database import db
from datetime import datetime

class Applications(db.Model):
    id =  db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    Request = db.Column(db.String(100))
    Duration = db.Column(db.String(100))
    Application_time = db.Column(db.DateTime, default = datetime.utcnow)
    Status = db.Column(db.String(100))