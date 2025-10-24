# routes/teacher_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Teacher
from models import Transaction

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@teacher_bp.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form.get('name')
        salary = float(request.form.get('salary') or 0)
        t = Teacher(name=name, salary=salary)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('teacher_bp.teachers'))
    return render_template('form.html', title='Add Teacher')

@teacher_bp.route('/edit_teacher/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    t = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        t.name = request.form.get('name')
        t.salary = float(request.form.get('salary') or 0)
        db.session.commit()
        return redirect(url_for('teacher_bp.teachers'))
    return render_template('form.html', title='Edit Teacher', obj=t)

@teacher_bp.route('/delete_teacher/<int:id>')
def delete_teacher(id):
    t = Teacher.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('teacher_bp.teachers'))
