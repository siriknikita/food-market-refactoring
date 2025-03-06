import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError

from market.forms import RegisterForm
from market.models import User
from market.constants import ERROR_MESSAGES
from market.extensions import db


class TestForms(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SECRET_KEY'] = 'test_secret'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for tests
        self.db = db
        self.db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_validate_username_exists(self):
        user = User(name='testuser', email='test@example.com',
                    password_hash='hashed_password')
        self.db.session.add(user)
        self.db.session.commit()

        form = RegisterForm()
        form.username.data = 'testuser'

        with self.app.test_request_context():
            with self.assertRaises(ValidationError) as context:
                form.validate_username(form.username)

            self.assertEqual(str(context.exception),
                             ERROR_MESSAGES['username_exists'])

    def test_validate_username_not_exists(self):
        form = RegisterForm()
        form.username.data = 'newuser'
        with self.app.test_request_context():
            try:
                form.validate_username(form.username)
            except ValidationError:
                self.fail("ValidationError raised unexpectedly")

    def test_validate_email_exists(self):
        user = User(name='testuser', email='test@example.com',
                    password_hash='hashed_password')
        self.db.session.add(user)
        self.db.session.commit()

        form = RegisterForm()
        form.email_address.data = 'test@example.com'
        with self.app.test_request_context():
            with self.assertRaises(ValidationError) as context:
                form.validate_email_address(form.email_address)

            self.assertEqual(str(context.exception),
                             ERROR_MESSAGES['email_exists'])

    def test_validate_email_not_exists(self):
        form = RegisterForm()
        form.email_address.data = 'new@example.com'
        with self.app.test_request_context():
            try:
                form.validate_email_address(form.email_address)
            except ValidationError:
                self.fail("ValidationError raised unexpectedly")

    def test_register_form_validators(self):
        with self.app.test_request_context():
            form = RegisterForm()
            form.username.data = 'testuser'
            form.email_address.data = 'test@example.com'
            form.password1.data = 'password123'
            form.password2.data = 'password123'
            form.phone.data = "1234567890"

            user1 = User(name='existuser', email='exist@example.com',
                         password_hash='hashed_password')
            self.db.session.add(user1)
            self.db.session.commit()

            form.username.data = 'existuser'
            self.assertFalse(form.validate())
            self.assertEqual(form.username.errors, [
                             ERROR_MESSAGES['username_exists']])

            form.username.data = 'testuser'
            form.email_address.data = 'exist@example.com'
            self.assertFalse(form.validate())
            self.assertEqual(form.email_address.errors, [
                             ERROR_MESSAGES['email_exists']])

            form.email_address.data = 'test@example.com'
            form.password2.data = "password1234"
            self.assertFalse(form.validate())
            self.assertEqual(form.password2.errors, [
                             "Field must be equal to password1."])

            form.password2.data = "password123"
            form.password1.data = "123"
            self.assertFalse(form.validate())
            self.assertEqual(form.password1.errors, [
                             "Field must be at least 6 characters long."])
            form.password1.data = "password123"
            self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()
