from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired

from .app import app
from .models import Tag, Subtag
from wtforms.fields import SelectMultipleField


class TagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Save')

    def save(self):
        tag = Tag(name=self.name.data)
        tag.save()



class PortfolioItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    short_desc = TextAreaField('Short Description', validators=[DataRequired()])
    long_desc = TextAreaField('Long Description', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    tags = SelectMultipleField('Tags', coerce=int)
    subtags = SelectMultipleField('Subtags', coerce=int)

    def __init__(self, *args, **kwargs):
        super(PortfolioItemForm, self).__init__(*args, **kwargs)


        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
        self.subtags.choices = [(subtag.id, subtag.name) for subtag in Subtag.query.all()]

        if kwargs.get('obj'):
            self.tags.data = [tag.id for tag in kwargs['obj'].tags]
            self.subtags.data = [subtag.id for subtag in kwargs['obj'].subtags]