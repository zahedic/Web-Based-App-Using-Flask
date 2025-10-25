from flask import Flask, render_template
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

# Seed default data (runs only if tables empty)
def seed_data():
    if not Student.query.first():
        s1 = Student(name="Awad Islam Chowdhury", course="Python", monthly_fee=5000)
        s2 = Student(name="Zawad Islam Chowdhury", course="Django", monthly_fee=6000)
        db.session.add_all([s1, s2])
        db.session.commit()
        db.session.add_all([
            Transaction(type='income', amount=s1.monthly_fee, description=f'{s1.name} paid for {s1.course}', student_id=s1.id),
            Transaction(type='income', amount=s2.monthly_fee, description=f'{s2.name} paid for {s2.course}', student_id=s2.id)
        ])
        db.session.commit()

    if not Teacher.query.first():
        t1 = Teacher(name="Mr. Hasan", salary=8000)
        t2 = Teacher(name="Mrs. Fatema", salary=8500)
        db.session.add_all([t1, t2])
        db.session.commit()
        db.session.add_all([
            Transaction(type='expense', amount=t1.salary, description=f'Salary paid to Teacher {t1.name}', teacher_id=t1.id),
            Transaction(type='expense', amount=t2.salary, description=f'Salary paid to Teacher {t2.name}', teacher_id=t2.id)
        ])
        db.session.commit()

    if not Employee.query.first():
        e1 = Employee(name="Rahim", salary=4000)
        e2 = Employee(name="Karina", salary=4500)
        db.session.add_all([e1, e2])
        db.session.commit()
        db.session.add_all([
            Transaction(type='expense', amount=e1.salary, description=f'Salary paid to Employee {e1.name}', employee_id=e1.id),
            Transaction(type='expense', amount=e2.salary, description=f'Salary paid to Employee {e2.name}', employee_id=e2.id)
        ])
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
