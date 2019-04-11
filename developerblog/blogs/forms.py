from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


from flask_login import current_user
from developerblog.models import BlogPost


class BlogPostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    text  = TextAreaField('Text', validators= [DataRequired()])
    submit = SubmitField('Create')
