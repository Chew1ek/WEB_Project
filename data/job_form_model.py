from flask_wtf import *
from flask_wtf.file import *
from wtforms import *
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    description = StringField('Описание предмета', validators=[DataRequired()])
    item_name = StringField('Название предмета', validators=[DataRequired()])
    price = IntegerField("Цена в рублях", validators=[DataRequired()])
    submit = SubmitField('Выставить на продажу')
    image = FileField('Изображение товара', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'],
                                                                                    'Только изображения (jpg, jpeg, png)!')])