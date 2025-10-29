from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Transaction, Student, Teacher, Employee
from datetime import datetime

transaction_bp = Blueprint('transaction_bp', __name__, url_prefix='/transactions')

@transaction_bp.route('/')
def list_transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=transactions)

@transaction_bp.route('/add', methods=['GET', 'POST'])
def add_transaction():
    students = Student.query.all()
    teachers = Teacher.query.all()
    employees = Employee.query.all()

    if request.method == 'POST':
        type_ = request.form['type']
        amount = float(request.form['amount'])
        description = request.form['description']

        student_id = request.form.get('student_id') or None
        teacher_id = request.form.get('teacher_id') or None
        employee_id = request.form.get('employee_id') or None

        selected = [bool(student_id), bool(teacher_id), bool(employee_id)]
        if sum(selected) > 1:
            flash("Please select only one: Student OR Teacher OR Employee", "danger")
            return redirect(url_for('transaction_bp.add_transaction'))

        transaction = Transaction(
            type=type_,
            amount=amount,
            description=description,
            date=datetime.utcnow(),
            student_id=int(student_id) if student_id else None,
            teacher_id=int(teacher_id) if teacher_id else None,
            employee_id=int(employee_id) if employee_id else None
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transaction_bp.list_transactions'))

    return render_template('form.html', action='Add', kind='transaction', students=students, teachers=teachers, employees=employees)

@transaction_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    students = Student.query.all()
    teachers = Teacher.query.all()
    employees = Employee.query.all()

    if request.method == 'POST':
        transaction.type = request.form['type']
        transaction.amount = float(request.form['amount'])
        transaction.description = request.form['description']
        transaction.student_id = request.form.get('student_id') or None
        transaction.teacher_id = request.form.get('teacher_id') or None
        transaction.employee_id = request.form.get('employee_id') or None
        db.session.commit()
        return redirect(url_for('transaction_bp.list_transactions'))

    return render_template('form.html', action='Edit',kind='transaction', transaction=transaction, students=students, teachers=teachers, employees=employees)

@transaction_bp.route('/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('transaction_bp.list_transactions'))

@transaction_bp.route('/search')
def search_transaction():
    q = request.args.get('q','').strip()
    transaction = Transaction.query.filter(Transaction.name.contains(q)).all() if q else Transaction.query.all()
    return render_template('students.html', transaction=transaction, q=q)

