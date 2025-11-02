# Web-Based-App-Using-Flask
# NVIT  Management System
# --------------------- Import Required Modules ---------------------
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Student, Teacher, Employee, Transaction
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.employee_routes import employee_bp
from routes.transaction_routes import transaction_bp
from collections import OrderedDict

# --------------------- Initialize Flask application ---------------------
app = Flask(__name__)

# --------------------- Configure database URI and settings ---------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_vision.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

# --------------------- Initialize SQLAlchemy with the Flask app--------------------- 
db.init_app(app)

# --------------------- Register Blueprints for modular routing ---------------------
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(transaction_bp)

# --------------------- Dashboard Route ---------------------
@app.route('/')
def dashboard():
    # --------------------- Calculate total income and expense from transactions
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type=='income').scalar() or 0
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.type=='expense').scalar() or 0
    balance = total_income - total_expense  # Compute current balance

    # --------------------- Fetch all transactions ordered by date ---------------------
    rows = Transaction.query.order_by(Transaction.date.asc()).all()
    
    # --------------------- Group transactions by date ---------------------
    grouped = OrderedDict()
    for t in rows:
        key = t.date.strftime('%B %Y')                       # Format Month & Year in X-axis
        if key not in grouped:
            grouped[key] = {'income': 0, 'expense': 0}
        if t.type == 'income':
            grouped[key]['income'] += t.amount
        else:
            grouped[key]['expense'] += t.amount

    # --------------------- Prepare data for charts ---------------------
    labels = list(grouped.keys())                               # Dates for x-axis
    income_data = [grouped[d]['income'] for d in labels]        # Income per date
    expense_data = [grouped[d]['expense'] for d in labels]      # Expense per date

    # --------------------- Render the dashboard template with computed values ---------------------
    return render_template(
        'dashboard.html',
        income=round(total_income, 2),
        expense=round(total_expense, 2),
        balance=round(balance, 2),
        labels=labels,
        income_data=income_data,
        expense_data=expense_data
    )

# --------------------- Edit Route ---------------------
@app.route('/edit/<kind>/<int:id>', methods=['GET', 'POST'])
def edit(kind, id):
    # --------------------- Load the appropriate object based on the kind parameter ---------------------
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
        flash('Unknown kind', 'danger')                         # Invalid kind
        return redirect(url_for('dashboard'))

    # --------------------- Handle form submission (POST request) ---------------------
    if request.method == 'POST':
        try:
            if kind == 'student':
                # --------------------- Update student fields ---------------------
                obj.name = request.form.get('name', obj.name)
                obj.course = request.form.get('course', obj.course)
                fee = request.form.get('monthly_fee', '')
                obj.monthly_fee = float(fee) if fee.strip() != '' else None

            elif kind == 'teacher':
                # --------------------- Update teacher fields ---------------------
                obj.name = request.form.get('name', obj.name)
                sal = request.form.get('salary', '')
                obj.salary = float(sal) if sal.strip() != '' else None

            elif kind == 'employee':
                # --------------------- Update employee fields ---------------------
                obj.name = request.form.get('name', obj.name)
                sal = request.form.get('salary', '')
                obj.salary = float(sal) if sal.strip() != '' else None

            elif kind == 'transaction':
                # --------------------- Update transaction fields ---------------------
                obj.type = request.form.get('type', obj.type)
                amt = request.form.get('amount', '')
                obj.amount = float(amt) if amt.strip() != '' else 0.0
                obj.description = request.form.get('description', obj.description)

                # --------------------- Convert empty string IDs to None ---------------------
                sid = request.form.get('student_id') or None
                tid = request.form.get('teacher_id') or None
                eid = request.form.get('employee_id') or None

                obj.student_id = int(sid) if sid else None
                obj.teacher_id = int(tid) if tid else None
                obj.employee_id = int(eid) if eid else None

            # --------------------- Commit updates to database ---------------------
            db.session.commit()
            return redirect(url_for('dashboard'))
        except ValueError:
            # --------------------- Rollback if invalid numeric value is provided ---------------------
            db.session.rollback()

    # --------------------- Handle GET request: fetch lists for dropdowns ---------------------
    students = Student.query.all()
    teachers = Teacher.query.all()
    employees = Employee.query.all()

    # --------------------- Render form template with object data and lists ---------------------
    return render_template(
        'form.html',
        title=f'Edit {kind.title()}',
        kind=kind,
        obj=obj,
        students=students,
        teachers=teachers,
        employees=employees
    )

# --------------------- Main Entry Point ---------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()                         # Create tables if not exist
    app.run(debug=True)                         # Run Flask app in debug mode


