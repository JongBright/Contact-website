from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length, Email


class Delete(FlaskForm):
    fn2 = StringField("First Name: ", validators=[DataRequired(), length(min=2, max=10)])
    ln2 = StringField("Last Name: ", validators=[DataRequired(), length(min=2, max=10)])
    email2 = StringField("Email: ", validators=[DataRequired(), Email()])
    submit2 = SubmitField("Delete")





