# routes/student_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@student_bp.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        course = request.form.get('course')
        fee = request.form.get('monthly_fee') or 0
        s = Student(name=name, course=course, monthly_fee=float(fee))
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('student_bp.students'))
    return render_template('form.html', title='Add Student')

@student_bp.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    s = Student.query.get_or_404(id)
    if request.method == 'POST':
        s.name = request.form.get('name')
        s.course = request.form.get('course')
        s.monthly_fee = float(request.form.get('monthly_fee') or 0)
        db.session.commit()
        return redirect(url_for('student_bp.students'))
    return render_template('form.html', title='Edit Student', obj=s)

@student_bp.route('/delete_student/<int:id>')
def delete_student(id):
    s = Student.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('student_bp.students'))
