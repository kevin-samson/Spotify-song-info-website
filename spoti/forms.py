from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MainForm(FlaskForm):
    website = StringField('Spotify URL')
    submit = SubmitField('Submit')
    submit2 = SubmitField('Get info of current song')