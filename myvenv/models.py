from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course = db.Column(db.String(100))
    monthly_fee = db.Column(db.Float)
    transactions = db.relationship('Transaction', backref='student', lazy=True)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    salary = db.Column(db.Float)
    transactions = db.relationship('Transaction', backref='teacher', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    salary = db.Column(db.Float)
    transactions = db.relationship('Transaction', backref='employee', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # Income or Expense
    amount = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
