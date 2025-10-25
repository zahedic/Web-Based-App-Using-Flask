# routes/teacher_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Teacher, Transaction

teacher_bp = Blueprint('teacher_bp', __name__, url_prefix='/teachers')

@teacher_bp.route('/')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@teacher_bp.route('/add', methods=['GET','POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form.get('name')
        salary = float(request.form.get('salary') or 0)
        t = Teacher(name=name, salary=salary)
        db.session.add(t)
        db.session.commit()
        # add expense transaction
        tr = Transaction(type='expense', amount=salary, description=f'Salary paid to Teacher {name}', teacher_id=t.id)
        db.session.add(tr)
        db.session.commit()
        return redirect(url_for('teacher_bp.teachers'))
    return render_template('form.html', title='Add Teacher', kind='teacher')

@teacher_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_teacher(id):
    t = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        old_name = t.name
        t.name = request.form.get('name')
        t.salary = float(request.form.get('salary') or 0)
        db.session.commit()
        # update related expense transaction(s) for this teacher (simple heuristic)
        Transaction.query.filter(Transaction.teacher_id==t.id).update({
            Transaction.amount: t.salary,
            Transaction.description: f'Salary paid to Teacher {t.name}'
        })
        db.session.commit()
        return redirect(url_for('teacher_bp.teachers'))
    return render_template('form.html', title='Edit Teacher', kind='teacher', obj=t)

@teacher_bp.route('/delete/<int:id>')
def delete_teacher(id):
    t = Teacher.query.get_or_404(id)
    Transaction.query.filter(Transaction.teacher_id==t.id).delete()
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('teacher_bp.teachers'))

@teacher_bp.route('/search')
def search_teacher():
    q = request.args.get('q','').strip()
    teachers = Teacher.query.filter(Teacher.name.contains(q)).all() if q else Teacher.query.all()
    return render_template('teachers.html', teachers=teachers, q=q)
