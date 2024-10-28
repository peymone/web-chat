# Third party packages
from wtforms import Form
from wtforms.fields import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import InputRequired, Length, Optional, EqualTo


class RegistrationForm(Form):
    """Form for user's registration"""

    email = EmailField("Company Email", [InputRequired()], render_kw={"placeholder": "Company Email"})
    password = PasswordField("Password", [InputRequired(), Length(min=5), EqualTo('confirm', message="passwords must be equal")],
                             render_kw={"placeholder": "Password"})
    confirm = PasswordField("Confirm Password", render_kw={"placeholder": "Repeat Password"})
    full_name = StringField("Full Name", [InputRequired(), Length(min=5)], render_kw={"placeholder": "Full Name"})
    department = StringField("Company Department", [Optional()], default=None, render_kw={"placeholder": "Department (optional)"})
    department_role = StringField("Department Role", [Optional()], default=None, render_kw={"placeholder": "Department Role (optional)"})
    submit = SubmitField("Register")


class AuthentificationForm(Form):
    """Form for user's authentification"""

    email = EmailField("Email", [InputRequired()], render_kw={"placeholder": "Company Email"})
    password = PasswordField("Password", [InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Log In")
