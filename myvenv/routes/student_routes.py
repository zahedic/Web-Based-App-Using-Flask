# routes/student_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Student, Transaction

student_bp = Blueprint('student_bp', __name__, url_prefix='/students')

@student_bp.route('/')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@student_bp.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        course = request.form.get('course')
        fee = float(request.form.get('monthly_fee') or 0)
        s = Student(name=name, course=course, monthly_fee=fee)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('student_bp.students'))
    return render_template('form.html', title='Add Student', kind='student')

@student_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    s = Student.query.get_or_404(id)
    if request.method == 'POST':
        s.name = request.form.get('name')
        s.course = request.form.get('course')
        s.monthly_fee = float(request.form.get('monthly_fee') or 0)
        db.session.commit()
        
        return redirect(url_for('student_bp.students'))
    return render_template('form.html', title='Edit Student', kind='student', obj=s)

@student_bp.route('/delete/<int:id>')
def delete_student(id):
    s = Student.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('student_bp.students'))

@student_bp.route('/search')
def search_student():
    q = request.args.get('q','').strip()
    students = Student.query.filter(Student.name.contains(q)).all() if q else Student.query.all()
    return render_template('students.html', students=students, q=q)
