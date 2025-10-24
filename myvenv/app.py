# app.py
from flask import Flask, render_template
from datetime import datetime
from models import db, Student, Teacher, Employee, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_vision_it.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db with app
db.init_app(app)

# import blueprints (after db/init)
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.employee_routes import employee_bp
from routes.transaction_routes import transaction_bp

app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(transaction_bp)

@app.route('/')
def dashboard():
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'income').scalar() or 0
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type == 'expense').scalar() or 0
    balance = total_income - total_expense

    # prepare chart data grouped by date (day)
    rows = db.session.query(Transaction.date, Transaction.type, Transaction.amount).order_by(Transaction.date.asc()).all()
    # aggregate by date label:
    labels = []
    income_map = {}
    expense_map = {}
    for d, ttype, amt in [(r[0].strftime('%Y-%m-%d'), r[1], r[2]) for r in rows]:
        labels.append(d)
    # unique ordered labels
    labels = sorted(list(dict.fromkeys(labels)))
    for l in labels:
        income_map[l] = 0
        expense_map[l] = 0
    for r in rows:
        l = r[0].strftime('%Y-%m-%d')
        if r[1] == 'income':
            income_map[l] += r[2]
        else:
            expense_map[l] += r[2]
    income_data = [income_map[l] for l in labels]
    expense_data = [expense_map[l] for l in labels]

    return render_template('dashboard.html',
                           income=round(total_income,2),
                           expense=round(total_expense,2),
                           balance=round(balance,2),
                           labels=labels,
                           income_data=income_data,
                           expense_data=expense_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
