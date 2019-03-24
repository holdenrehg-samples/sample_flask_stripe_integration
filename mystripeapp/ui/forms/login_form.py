from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from mystripeapp import models


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])

    def validate(self):
        """
        Adds additional validation to the form.

        :return {bool}: Returns True if successful.
        """
        rv = super().validate()
        if not rv:
            return False

        user = models.User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append("That email is not valid in our system.")
            return False

        if not user.check_password(self.password.data):
            self.email.errors.append("There was a problem logging in with those credentials")
            return False

        self.user = user
        return True
