# routes/transaction_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Transaction, Student

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/transactions')
def transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=transactions)

@transaction_bp.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    students = Student.query.all()
    if request.method == 'POST':
        type_ = request.form.get('type')
        amount = float(request.form.get('amount') or 0)
        description = request.form.get('description')
        student_id = request.form.get('student_id') or None
        t = Transaction(type=type_, amount=amount, description=description,
                        student_id=int(student_id) if student_id else None)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('transaction_bp.transactions'))
    return render_template('form.html', title='Add Transaction', students=students)

@transaction_bp.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    t = Transaction.query.get_or_404(id)
    students = Student.query.all()
    if request.method == 'POST':
        t.type = request.form.get('type')
        t.amount = float(request.form.get('amount') or 0)
        t.description = request.form.get('description')
        student_id = request.form.get('student_id') or None
        t.student_id = int(student_id) if student_id else None
        db.session.commit()
        return redirect(url_for('transaction_bp.transactions'))
    return render_template('form.html', title='Edit Transaction', obj=t, students=students)

@transaction_bp.route('/delete_transaction/<int:id>')
def delete_transaction(id):
    t = Transaction.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('transaction_bp.transactions'))
