from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flask_wtf import FlaskForm
from market.constants import ERROR_MESSAGES
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(name=username_to_check.data).first()
        if user:
            raise ValidationError(ERROR_MESSAGES['username_exists'])

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError(ERROR_MESSAGES['email_exists'])

    username = StringField(label='Ім\'я користувача:', validators=[
        Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Електронна пошта:', validators=[
        Email(), DataRequired()])
    phone = StringField(label='Номер телефону:')
    password1 = PasswordField(label='Пароль:', validators=[
        Length(min=6), DataRequired()])
    password2 = PasswordField(label='Підтвердіть пароль:', validators=[
        EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Створити акаунт')


class LoginForm(FlaskForm):
    username = StringField(label='Ім\'я користувача:',
                           validators=[DataRequired()])
    password = PasswordField(label='Пароль:', validators=[DataRequired()])
    submit = SubmitField(label='Увійти')


class AddingForm(FlaskForm):
    submit = SubmitField(label='Додати у кошик')


class SubmitOrderForm(FlaskForm):
    submit = SubmitField('Підтвердити замовлення')
