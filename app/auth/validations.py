# Third party packages
from wtforms import Form
from wtforms.fields import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import InputRequired, Length, Optional, EqualTo


class RegistrationForm(Form):
    """Form for user's registration"""

    email = EmailField("Company Email", [InputRequired()])
    password = PasswordField("Password", [InputRequired(), Length(min=5), EqualTo('confirm', message="passwords must be equal")])
    confirm = PasswordField("Confirm Password")
    full_name = StringField("Full Name", [InputRequired(), Length(min=5)])
    department = StringField("Company Department", [Optional()], default=None)
    department_role = StringField("Department Role", [Optional()], default=None)
    submit = SubmitField("Register")


class AuthentificationForm(Form):
    """Form for user's authentification"""

    email = EmailField("Company Email", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField("LogIn")
