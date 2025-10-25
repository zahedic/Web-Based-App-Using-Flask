from flask import Flask, render_template,request,flash,redirect,url_for
from models import db, Student, Teacher, Employee, Transaction
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.employee_routes import employee_bp
from routes.transaction_routes import transaction_bp
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_vision.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register Blueprints
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(transaction_bp)

@app.route('/')
def dashboard():
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type=='income').scalar() or 0
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type=='expense').scalar() or 0
    balance = total_income - total_expense

    rows = Transaction.query.order_by(Transaction.date.asc()).all()
    grouped = OrderedDict()
    for t in rows:
        key = t.date.strftime('%Y-%m-%d')
        if key not in grouped:
            grouped[key] = {'income': 0, 'expense': 0}
        if t.type == 'income':
            grouped[key]['income'] += t.amount
        else:
            grouped[key]['expense'] += t.amount

    labels = list(grouped.keys())
    income_data = [grouped[d]['income'] for d in labels]
    expense_data = [grouped[d]['expense'] for d in labels]

    return render_template('dashboard.html',
                           income=round(total_income,2),
                           expense=round(total_expense,2),
                           balance=round(balance,2),
                           labels=labels,
                           income_data=income_data,
                           expense_data=expense_data)

@app.route('/edit/<kind>/<int:id>', methods=['GET', 'POST'])
def edit(kind, id):
    # load object by kind
    obj = None
    if kind == 'student':
        obj = Student.query.get_or_404(id)
    elif kind == 'teacher':
        obj = Teacher.query.get_or_404(id)
    elif kind == 'employee':
        obj = Employee.query.get_or_404(id)
    elif kind == 'transaction':
        obj = Transaction.query.get_or_404(id)
    else:
        flash('Unknown kind', 'danger')
        return redirect(url_for('dashboard'))

    # POST: update fields (use request.form.get to avoid KeyError)
    if request.method == 'POST':
        try:
            if kind == 'student':
                obj.name = request.form.get('name', obj.name)
                obj.course = request.form.get('course', obj.course)
                fee = request.form.get('monthly_fee', '')
                obj.monthly_fee = float(fee) if fee.strip() != '' else None

            elif kind == 'teacher':
                obj.name = request.form.get('name', obj.name)
                sal = request.form.get('salary', '')
                obj.salary = float(sal) if sal.strip() != '' else None

            elif kind == 'employee':
                obj.name = request.form.get('name', obj.name)
                sal = request.form.get('salary', '')
                obj.salary = float(sal) if sal.strip() != '' else None

            elif kind == 'transaction':
                obj.type = request.form.get('type', obj.type)
                amt = request.form.get('amount', '')
                obj.amount = float(amt) if amt.strip() != '' else 0.0
                obj.description = request.form.get('description', obj.description)

                # student/teacher/employee ids might be empty string -> convert to None
                sid = request.form.get('student_id') or None
                tid = request.form.get('teacher_id') or None
                eid = request.form.get('employee_id') or None

                obj.student_id = int(sid) if sid else None
                obj.teacher_id = int(tid) if tid else None
                obj.employee_id = int(eid) if eid else None

            db.session.commit()
            return redirect(url_for('dashboard'))
        except ValueError:
            # e.g. invalid number in amount/salary
            db.session.rollback()
            

    # GET: render form with lists for selects (for transactions)
    students = Student.query.all()
    teachers = Teacher.query.all()
    employees = Employee.query.all()

    return render_template(
        'form.html',
        title=f'Edit {kind.title()}',
        kind=kind,
        obj=obj,
        students=students,
        teachers=teachers,
        employees=employees
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
