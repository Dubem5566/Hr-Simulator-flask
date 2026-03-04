from flask import Flask, redirect, render_template, url_for, session, request , flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate # type: ignore
from sqlalchemy import or_
from models import db, Employee
from models import db, Transaction
from models import db, Clockin
from models import db, Applications
from models import db, Sal_req
import random
import string
import os

app = Flask(__name__)
# Session Secret Key
app.secret_key = "my_secret_key_123"
# For creating database path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "hr.db")
db.init_app(app)
migrate = Migrate(app,db)

ran = string.digits    # For generating random digits

admin_logs = {"Philip":"65748", "Obinna":"77388"}  # Admin login details

records = []   # For temporarily storing employee requests


@app.route("/")

def reroute() :
    return redirect(url_for("home"))

@app.route("/home")

def home():
    return render_template("home.html", admin_logs = admin_logs)

@app.route("/admin/login", methods = ["POST","GET"])

def admin_login():
    if request.method == "POST" :
        username = request.form["manager_username"]
        password = request.form["manager_pass"]
        if username in admin_logs :
            if password == admin_logs.get(username) :
                session["Name"] = username
                flash("Login Successful!", "success")
                return redirect(url_for("admin"))
            else :
                flash("Incorrect Password!", "error")
                return redirect(url_for("admin_login"))
            
        elif username not in admin_logs :
            flash("Incorrect Username!", "error")
            return redirect(url_for("admin_login"))

        elif username not in admin_logs and password is not admin_logs.get(username) :
              flash("Invalid Credentials!", "error")
              return redirect(url_for("admin_login"))
        
    return render_template("admin_pass.html")

@app.route('/admin', methods=["POST","GET"])

def admin():
    return render_template("admin.html", name = session["Name"])

@app.route("/signout", methods=["POST","GET"])

def signout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/register", methods = ["POST", "GET"])

def reg_employee():
    if request.method == "POST" :
        fn = request.form["First Name"]
        ln = request.form["Last Name"]
        g = request.form["Gender"]
        dob = request.form["D.O.B"]
        number = request.form["Phone Number"]
        email = request.form["email"]

        employees = Employee (
            First_name = fn,
            Last_name = ln,
            Gender = g,
            DOB = dob,
            Phone_Number = number,
            Email = email
        )
        db.session.add(employees)
        db.session.commit()

        session["First Name"] = fn
        return redirect(url_for("reg_2"))

    return render_template("register.html")

@app.route("/reg2", methods = ["POST", "GET"])

def reg_2():
    search = Employee.query.filter_by(First_name = session["First Name"]).all()
    if request.method == "POST" :
        dept = request.form["department"]
        emp_type = request.form["employment type"]

        for s in search :
            s.Department = dept
            s.Employment_type = emp_type

            db.session.commit()
            return redirect(url_for("Generate_id"))
    
    return render_template("reg2.html")

@app.route("/generate/id", methods=["POST","GET"])

def Generate_id() :
    possible_id = "".join(random.choices(ran, k=4))
    search = Employee.query.filter_by(First_name = session["First Name"]).all()
    for s in search :
        if s.Department == "Tech" :
            s.I_D = f"TCH-{possible_id}"
            s.Basic_salary = 100
            db.session.commit()
            session["I.D"] = s.I_D
            session["sal"] = s.Basic_salary
        else :
            s.I_D = f"MKT-{possible_id}"
            s.Basic_salary = 80
            db.session.commit()
            session["I.D"] = s.I_D
            session["sal"] = s.Basic_salary
        return redirect(url_for("reg_3"))

@app.route("/reg3", methods = ["POST", "GET"])

def reg_3():
    search = Employee.query.filter_by(First_name = session["First Name"]).all()
    if request.method == "POST" :
        id = request.form["emp_id"]
        sal = request.form["Salary"]
        freq = request.form["Salary frequency"]
        bn = request.form["Bank Name"]
        acc = request.form["Account Number"]

        for s in search :
            s.I_D = id
            s.Basic_salary = sal
            s.Salary_Frequency = freq
            s.Bank_Name = bn
            s.Account_Number = acc
            s.Balance = 0

            db.session.commit()
            return redirect(url_for("reg_4"))
    
    return render_template("reg3.html", emp_id = session["I.D"], salary = session["sal"])

@app.route("/reg4", methods = ["POST", "GET"])

def reg_4 ():
    search = Employee.query.filter_by(First_name = session["First Name"])
    if request.method == "POST" :
        n = request.form["Nationality"]
        t = request.form["State"]
        c = request.form["City"]
        a = request.form["Address"]

        for s in search :
            s.Nationality = n
            s.State = t
            s.City = c 
            s.Address = a 

            db.session.commit()
            return redirect(url_for("reg_5"))
    
    return render_template("reg4.html")

@app.route("/reg5", methods = ["POST", "GET"])

def reg_5 ():
    search = Employee.query.filter_by(First_name = session["First Name"]).all()
    if request.method == "POST" :
        n = request.form["Name"]
        rel = request.form["Relationship"]
        num = request.form["Number"]
        add = request.form["Kin Address"]

        for s in search :
            s.Next_of_kin = n 
            s.Relationship = rel 
            s.number = num 
            s.addres = add 
            s.No_of_clockin = 0

            db.session.commit()
            return redirect(url_for("reg_6"))
    
    return render_template("reg5.html")

@app.route("/reg6", methods = ["POST", "GET"])

def reg_6 ():
    search = Employee.query.filter_by(First_name = session["First Name"]).all()
    if request.method == "POST" :
        un = request.form["Username"]
        pw = request.form["Password"]
        if len(pw) >= 5 :
          hashed_password = generate_password_hash(pw)  # Hashing of password

          for s in search :
            s.Username = un 
            s.Password = hashed_password

            db.session.commit()
            flash("Registration was successful!" , "success")
            return redirect(url_for("admin"))
        else :
            flash("Password must be at least 5 characters!", "warning")
            return redirect(url_for("reg_6"))
    
    return render_template("reg6.html")

@app.route('/login', methods=["POST","GET"])

def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["pass"]
        s = Employee.query.filter_by(Username = user).first()  # Checking if username exists in database
        if s :
            if check_password_hash(s.Password,password) :  # Checking if hashed password of the password in db and the one the user entered matches
                session["nm"] = s.First_name
                session["dept"] = s.Department
                session["id"] = s.id
                flash("Login Successful!", "success")
                return redirect(url_for("employee_page"))
            else :
                flash("Incorrect Password!", "error")
                return redirect(url_for("login"))
            
        elif not s :
            flash("Incorrect Username!", "error")
            return redirect(url_for("login"))
   
    return render_template("login.html")

@app.route('/employee/page', methods=["POST","GET"])

def employee_page() :
    return render_template("employee.html", name = session["nm"])


@app.route('/clockin', methods = ["POST", "GET"])

def clock_in():
    if request.method == "POST" :
        name = request.form["name"]
        
        # Searching for employee name and date of clockin if any to confirm if employee has clocked in for the day
        current_time = datetime.now().date()
        existing = Clockin.query.filter( 
            Clockin.Name == name,
            db.func.date(Clockin.Clock_in_time)==current_time).first()
        
         #If employee has clocked in for the day
        if existing :
            flash("You've already clocked in for today!", "warning")
            return redirect(url_for("employee_page"))
        
        else :
            clockin = Clockin(
                Name = name ,
                Clock_in_time = current_time,
                Department = session["dept"]
                )
            db.session.add(clockin)
            db.session.commit()
            flash("You've successfully clocked in!" , "success")
            
            # Updating the number of clockin for that employee to the employee db
            search = Employee.query.filter_by(First_name = session["nm"]).first()
            search.No_of_clockin = search.No_of_clockin + 1
            db.session.commit()
            print(search.No_of_clockin)
            return redirect(url_for("employee_page"))

    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")  # Current time
    formatted_date = current_time.strftime("%d-%m-%Y") # Current date
    return render_template("clock_in.html", time = formatted_time, date = formatted_date , name = session["nm"])

@app.route('/application', methods = ["POST", "GET"])

def applications():
    if request.method == "POST" :
        nm = request.form["name"]
        dept = request.form["dept"]
        application = request.form["Application Type"]
        duration = request.form["Duration"]
        dur = request.form["Dur"]

        current_time = datetime.now()

        req = Applications(
            Name = nm ,
            Department = dept ,
            Request = application ,
            Duration = f"{str(duration)} {dur}" , 
            Application_time = current_time,
            Status = "Pending"
        )
        db.session.add(req)
        db.session.commit()
        flash("Your request has been sent!" , "success")
        return redirect(url_for("employee_page"))
    
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")
    formatted_date = current_time.strftime("%d-%m-%Y")
    return render_template("applications.html", time = formatted_time, date = formatted_date, name = session["nm"], dept = session["dept"])

@app.route("/approve_req")

def approve_req():
    s = Applications.query.filter_by(Status = "Pending").all()
    if s :
        for i in s :
            if i.Application_time :
               i.Application_time = i.Application_time.strftime("%d-%m-%Y")
        return render_template("approve_req.html", content = s)
    
    else :
        return render_template("empty_req.html")

@app.route("/approve/<int:index>")

def Approve(index) :
    s = Applications.query.filter_by(id = index).first()
    s.Status = "Approved"
    db.session.commit()
    flash("Request has been approved!", "success")
    return redirect(url_for("approve_req"))

@app.route("/reject/<int:index>")

def Reject(index):
    s = Applications.query.filter_by(id = index).first()
    s.Status = "Rejected"
    db.session.commit()
    flash("Request has been rejected!", "success")
    return redirect(url_for("approve_req"))

@app.route('/application/update')

def app_update():
    s = Applications.query.filter( or_ 
                                  (Applications.Status == "Approved",
                                   Applications.Status == "Rejected")
                                   ).all()
    if s :
        return render_template("application_update.html", content = s)
    
    else :
        return render_template("empty_req_update.html")

@app.route('/requestSalary', methods = ["POST", "GET"])

def req_sal():
    if request.method == "POST" :
        nm = request.form["Name"]
        id = request.form["ID"]
        dept = request.form["Department"]

        sal_det = Sal_req(
            I_D = id,
            Name = nm,
            Department = dept,
            Request = "Requested for payment"
        )
        db.session.add(sal_det)
        db.session.commit()
        flash("Your payment request has been sent!", "success")
        return redirect(url_for("employee_page"))

    s = Employee.query.filter_by(First_name = session["nm"]).first()
    return render_template("request_salary.html", name = session["nm"], dept = session["dept"], id = s.I_D)

@app.route('/check salary requests')

def check_salary_requests () :
    s = Sal_req.query.all()
    if s :
       return render_template("check_salary.html", requests = s)
    else :
        return render_template("check_salary.html")

@app.route("/paysalary")

def pay_sal():
    s = Employee.query.filter(Employee.No_of_clockin > 0).all()
    if s :
       for sa in s :
           salary = sa.Basic_salary * sa.No_of_clockin
       return render_template("pay_sal.html", content = s, sal = salary)
       
    else:
        return render_template("pay_sal.html")
    
@app.route("/pay/<int:index>")

def pay(index) :
    current_time = datetime.now()

    s = Employee.query.filter_by(id = index).first()
    salary =  s.Basic_salary * s.No_of_clockin
    s.Balance = s.Balance + salary
    db.session.commit()
    new_transaction = Transaction(
        employee_id = s.id,
        amount = salary,
        type = "Received Salary Payment",
        date = current_time,
        time = current_time
    )
    db.session.add(new_transaction)
    db.session.commit()

# Resetting the number of clockin to zero

    s = Employee.query.filter_by(id = index).first()
    s.No_of_clockin = 0
    db.session.commit()
    flash("Payment was successful", "success")
    return redirect(url_for("pay_sal"))
        

@app.route("/employeedetails", methods = ["POST", "GET"])

def employee_details():
    if request.method == "POST" :
        nm = request.form["query"]
        nm = nm.title()
        s = Employee.query.filter_by(First_name = nm).all()
        if s:
            return render_template("employee_search_result.html", content = s, employee = nm)
        else :
            flash("Employee does not exist!", "error")
            return redirect(url_for("employee_details"))
    
    s = Employee.query.all()
    if s :
        return render_template("employee_details.html", content = s)
    
    else :
        return render_template("empty_employee_details.html")

@app.route("/search/result", methods = ["POST", "GET"])

def search_result():
    if request.method == "POST" :
        nm = request.form["query"]
        nm = nm.title()
        s = Employee.query.filter_by(First_name = nm).all()
        if s:
            return render_template("employee_search_result.html", content = s, employee = nm)
        else :
            flash("Employee does not exist!", "error")
            return redirect(url_for("employee_details"))
        
@app.route('/balance')

def bal() :
    s = Employee.query.filter_by(id = session["id"]).first()
    if s.transactions :
       for txn in s.transactions:
           txn.date = txn.date.strftime("%d-%m-%Y")
           txn.time = txn.time.strftime("%I:%M %p")
       return render_template("balance.html", content = s.transactions, balance = s.Balance)
    else :
        return render_template("balance.html", balance = s.Balance)

@app.route("/transactions")

def trans() :
    s = Employee.query.filter_by(id = session["id"]).first()
    if s.transactions :
       for txn in s.transactions:
           txn.date = txn.date.strftime("%d-%m-%Y")
           txn.time = txn.time.strftime("%I:%M %p")
       return render_template("transaction_history.html", content = s.transactions)
    else:
        return render_template("transaction_history.html")



if __name__ == "__main__":
    app.run(port=5000)

