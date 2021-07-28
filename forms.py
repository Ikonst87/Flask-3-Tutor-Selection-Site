from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField, validators
from wtforms.fields.html5 import TelField


class BookingForm(FlaskForm):
    name = StringField(label='Вас зовут', validators=[validators.DataRequired()])
    phone = TelField(label='Ваш телефон',
                     validators=[validators.DataRequired()])
    day = HiddenField(label='day')
    time = HiddenField(label='time')
    tutor = HiddenField(label='tutor')
    submit = SubmitField(label='Записаться на пробный урок')


class RequestForm(FlaskForm):
    name = StringField(label="Вас зовут", validators=[validators.DataRequired()])
    phone = TelField(label='Ваш телефон',
                     validators=[validators.DataRequired()])
    submit = SubmitField(label="Найдите мне преподавателя")


class SortForm(FlaskForm):
    submit = SubmitField(label="Сортировать")
