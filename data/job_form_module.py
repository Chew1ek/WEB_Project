from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('ID начальника', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Время выполнения', validators=[DataRequired()])
    collaborators = StringField('ID рабочих', validators=[DataRequired()])
    work_done = BooleanField('Работа окончена?')
    submit = SubmitField('Отправить')
