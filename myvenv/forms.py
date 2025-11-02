# ------------------------- Import Required Modules -------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


# ------------------------- Transaction Form Definition -------------------------
# This form is used to create or edit a transaction (Income or Expense)

class TransactionForm(FlaskForm):
    # Transaction type: either 'income' or 'expense'
    type_ = SelectField('type', choices=[('income', 'income'), ('expense', 'expense')])

    # Amount field: must be a number (required)
    amount = FloatField('amount', validators=[DataRequired()])

    # Optional text field for transaction details
    description = StringField('Description', validators=[Optional()])

     # Optional dropdowns for linking a transaction to a specific person
    student_id = SelectField('Student (optional)', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher (optional)', coerce=int, validators=[Optional()])
    employee_id = SelectField('Employee (optional)', coerce=int, validators=[Optional()])

     # Submit button to save the form
    submit = SubmitField('Save')
