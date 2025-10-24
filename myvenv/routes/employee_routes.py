# routes/employee_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Employee

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@employee_bp.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        salary = float(request.form.get('salary') or 0)
        e = Employee(name=name, salary=salary)
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('employee_bp.employees'))
    return render_template('form.html', title='Add Employee')

@employee_bp.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    e = Employee.query.get_or_404(id)
    if request.method == 'POST':
        e.name = request.form.get('name')
        e.salary = float(request.form.get('salary') or 0)
        db.session.commit()
        return redirect(url_for('employee_bp.employees'))
    return render_template('form.html', title='Edit Employee', obj=e)

@employee_bp.route('/delete_employee/<int:id>')
def delete_employee(id):
    e = Employee.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('employee_bp.employees'))
