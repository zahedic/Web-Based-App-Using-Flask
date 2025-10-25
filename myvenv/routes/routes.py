from flask import render_template, redirect, url_for, request
from app import app, db
from models import Student, Teacher, Employee, Transaction
from forms import TransactionForm


@app.route('/transactions')
def transactions():
    all_transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=all_transactions)


@app.route('/transactions/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = TransactionForm(obj=transaction)

    # Dropdown choices
    form.student_id.choices = [(0, '-- None --')] + [(s.id, s.name) for s in Student.query.all()]
    form.teacher_id.choices = [(0, '-- None --')] + [(t.id, t.name) for t in Teacher.query.all()]
    form.employee_id.choices = [(0, '-- None --')] + [(e.id, e.name) for e in Employee.query.all()]

    if form.validate_on_submit():
        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.student_id = form.student_id.data or None
        transaction.teacher_id = form.teacher_id.data or None
        transaction.employee_id = form.employee_id.data or None
        db.session.commit()
        return redirect(url_for('transactions'))

    return render_template('edit_transaction.html', form=form)
