from .database import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer,primary_key=True)
    First_name = db.Column(db.String(100))
    Last_name = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    I_D = db.Column(db.String(50))
    Gender = db.Column(db.String(100))
    DOB = db.Column(db.String(100))
    Phone_Number = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Nationality = db.Column(db.String(100))
    State = db.Column(db.String(100))
    City = db.Column(db.String(100))
    Address = db.Column(db.String(100))
    Employment_type = db.Column(db.String(100))
    Basic_salary = db.Column(db.Integer)
    Salary_Frequency = db.Column(db.String(100))
    Bank_Name = db.Column(db.String(100))
    Account_Number = db.Column(db.String(100))
    Next_of_kin = db.Column(db.String(100))
    Relationship = db.Column(db.String(100))
    number = db.Column(db.String(100))
    addres = db.Column(db.String(100))
    Username = db.Column(db.String(100))
    Password = db.Column(db.String(200))
    No_of_clockin = db.Column(db.Integer, default = 0)
    Balance = db.Column(db.Integer, default=0)

    transactions = db.relationship("Transaction", backref="employee", order_by="desc(Transaction.date)", lazy=True)



class Transaction (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    amount = db.Column(db.Float, default=0)
    type = db.Column(db.String(50))  
    date = db.Column(db.DateTime, default=datetime.utcnow)
    time = db.Column(db.DateTime, default=datetime.utcnow)