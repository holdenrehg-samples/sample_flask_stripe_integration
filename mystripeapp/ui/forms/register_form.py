import stripe
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from werkzeug.security import generate_password_hash
from mystripeapp import models, utils
from mystripeapp.bootstrap import db


class RegisterForm(FlaskForm):

    name = StringField(
        "Name", validators=[validators.DataRequired(), validators.Length(min=1, max=64)]
    )
    email = StringField(
        "Email",
        validators=[
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=1, max=64),
        ],
    )
    password = PasswordField(
        "Password", validators=[validators.DataRequired(), validators.Length(min=8, max=64)]
    )
    stripeToken = PasswordField("Stripe Token", validators=[validators.DataRequired()])
    lastFour = PasswordField("Last Four", validators=[validators.DataRequired()])

    def validate(self):
        """
        Adds additional validation to the form.

        :return {bool}: Returns True if successful.
        """
        rv = super().validate()
        if not rv:
            return False

        user = models.User.query.filter_by(email=self.email.data).first()
        if user is not None:
            self.email.errors.append("The email address has already been taken.")
            return False

        return True

    def register_to_stripe(self, user):
        """
        Registers a user to stripe.

        :param user {models.User}: The user to register to stripe.
        :return {tuple}: Returns the customer and the subscription created.
        """
        env = utils.environment()
        stripe.api_key = env["billing"]["stripe"]["token"]

        customer = stripe.Customer.create(
            description=self.name.data,
            source=self.stripeToken.data,
            metadata={"customer_code": user.id},
        )

        subscription = stripe.Subscription.create(
            customer=customer.id, items=[{"plan": env["billing"]["stripe"]["product"]}]
        )

        return customer, subscription

    def create_user(self):
        """
        Creates a new user from the form data.

        :return {models.User}: Returns the user record created.
        """
        user = models.User(
            name=self.name.data,
            email=self.email.data,
            password=self.password.data,
            stripe_token=self.stripeToken.data,
            last_four=self.lastFour.data,
        )

        stripe_data = self.register_to_stripe(user)
        user.stripe_customer_id = stripe_data[0].id

        db.session.add(user)
        db.session.commit()

        return user
