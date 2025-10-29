# -------------------- Import Libraries --------------------
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# -------------------- Initialize Database --------------------
db = SQLAlchemy()

# -------------------- Student model --------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # Student ID
    name = db.Column(db.String(100))                    # Name
    course = db.Column(db.String(100))                  # Course
    monthly_fee = db.Column(db.Float)                   # Fee
    transactions = db.relationship('Transaction', backref='student', lazy=True)  # Linked transactions

# -------------------- Teacher model --------------------
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # Teacher ID
    name = db.Column(db.String(100))                    # Name
    subject = db.Column(db.String(100))                 # Subject
    salary = db.Column(db.Float)                        # Salary
    transactions = db.relationship('Transaction', backref='teacher', lazy=True)  # Linked transactions

# -------------------- Employee model --------------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # Employee ID
    name = db.Column(db.String(100))                    # Name
    role = db.Column(db.String(100))                    # Role
    salary = db.Column(db.Float)                        # Salary
    transactions = db.relationship('Transaction', backref='employee', lazy=True)  # Linked transactions

# -------------------- Transaction model --------------------
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # Transaction ID
    type = db.Column(db.String(50))                     # Income/Expense
    amount = db.Column(db.Float)                        # Amount
    date = db.Column(db.Date, default=datetime.utcnow)  # Date
    description = db.Column(db.String(200))             # Description

    # Foreign Keys --------------------
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
