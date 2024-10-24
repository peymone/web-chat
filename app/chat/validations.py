# Third party packages
from wtforms import Form
from wtforms.fields import PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Optional


class RoomForm(Form):
    """Accepts a room id and a password"""

    room = IntegerField('Room ID', [InputRequired()])
    password = PasswordField('Password', [Optional()])
    submit = SubmitField('EnterRoom')
