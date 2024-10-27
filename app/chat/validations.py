# Third party packages
from wtforms import Form
from wtforms.fields import PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Optional


class RoomForm(Form):
    """Accepts a room id and a password"""

    room = IntegerField('Room ID', [InputRequired()], render_kw={"placeholder": "Room ID"})
    password = PasswordField('Password', [Optional()], render_kw={"placeholder": "Password (Optional)"})
    submit = SubmitField('EnterRoom')
