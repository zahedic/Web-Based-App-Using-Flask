from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class TransactionForm(FlaskForm):
    type_ = SelectField('type', choices=[('income', 'income'), ('expense', 'expense')])
    amount = FloatField('amount', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])

    student_id = SelectField('Student (optional)', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher (optional)', coerce=int, validators=[Optional()])
    employee_id = SelectField('Employee (optional)', coerce=int, validators=[Optional()])

    submit = SubmitField('Save')
