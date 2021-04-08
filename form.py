from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length, Email


class Form(FlaskForm):
    fn = StringField("First Name: ", validators=[DataRequired(), length(min=2, max=10)])
    ln = StringField("Last Name: ", validators=[DataRequired(), length(min=2, max=10)])
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    tel = StringField("Phone: ", validators=[DataRequired(), length(min=7, max=20)])
    submit = SubmitField("Done")





