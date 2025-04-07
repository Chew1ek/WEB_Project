from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    description = StringField('Описание предмета', validators=[DataRequired()])
    seller_name = StringField('Продавец', validators=[DataRequired()])
    item_name = StringField('Название предмета', validators=[DataRequired()])
    submit = SubmitField('Добавить работу')



