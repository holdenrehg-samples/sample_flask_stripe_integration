import sqlalchemy
from flask import url_for
from flask_login.mixins import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import check_password_hash, generate_password_hash

from mystripeapp.bootstrap import app, db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    def __init__(self, password=None, *args, **kwargs):
        """
        On user initialization, we assume that the passwords are being passed
        in as plain-text from the registration form so we immediatley encrypt
        them before they hit the database.
        """
        if password:
            password = generate_password_hash(password)
        super().__init__(password=password, *args, **kwargs)

    @declared_attr
    def name(self):
        return sqlalchemy.Column(sqlalchemy.String(64), nullable=False)

    @declared_attr
    def email(self):
        return sqlalchemy.Column(sqlalchemy.String(64), nullable=False)

    @declared_attr
    def password(self):
        return sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    @declared_attr
    def stripe_token(self):
        return sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    @declared_attr
    def last_four(self):
        return sqlalchemy.Column(sqlalchemy.String(4), nullable=False)

    @declared_attr
    def stripe_customer_id(self):
        return sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    def check_password(self, password):
        """
        Check if a given plain text password matches the encrypted password that
        is currently stored in the database for this Team Member.

        :param password {str}: The password that we will check.
        :return {bool}: Returns True if the password matches.
        """
        if not self.password:
            return False
        return check_password_hash(self.password, password)
