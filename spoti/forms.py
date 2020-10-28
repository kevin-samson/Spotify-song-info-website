from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired


class MainForm(FlaskForm):
    website = StringField('Spotify URL or URI')
    submit = SubmitField('Submit')
    submit2 = SubmitField('Get info of the current song playing')

    def validate_website(self, website):
        if 'spotify' not in str(website):
            return ValidationError('That is not a Spotify URL')
