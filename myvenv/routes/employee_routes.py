# routes/employee_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Employee, Transaction

employee_bp = Blueprint('employee_bp', __name__, url_prefix='/employees')

@employee_bp.route('/')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@employee_bp.route('/add', methods=['GET','POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        salary = float(request.form.get('salary') or 0)
        e = Employee(name=name, salary=salary)
        db.session.add(e)
        db.session.commit()
        tr = Transaction(type='expense', amount=salary, description=f'Salary paid to Employee {name}', employee_id=e.id)
        db.session.add(tr)
        db.session.commit()
        return redirect(url_for('employee_bp.employees'))
    return render_template('form.html', title='Add Employee', kind='employee')

@employee_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_employee(id):
    e = Employee.query.get_or_404(id)
    if request.method == 'POST':
        e.name = request.form.get('name')
        e.salary = float(request.form.get('salary') or 0)
        db.session.commit()
        Transaction.query.filter(Transaction.employee_id==e.id).update({
            Transaction.amount: e.salary,
            Transaction.description: f'Salary paid to Employee {e.name}'
        })
        db.session.commit()
        return redirect(url_for('employee_bp.employees'))
    return render_template('form.html', title='Edit Employee', kind='employee', obj=e)

@employee_bp.route('/delete/<int:id>')
def delete_employee(id):
    e = Employee.query.get_or_404(id)
    Transaction.query.filter(Transaction.employee_id==e.id).delete()
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('employee_bp.employees'))

@employee_bp.route('/search')
def search_employee():
    q = request.args.get('q','').strip()
    employees = Employee.query.filter(Employee.name.contains(q)).all() if q else Employee.query.all()
    return render_template('employees.html', employees=employees, q=q)
