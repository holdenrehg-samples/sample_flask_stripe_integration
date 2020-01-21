import stripe
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound

from mystripeapp.bootstrap import app
from mystripeapp.ui.forms.login_form import LoginForm
from mystripeapp.ui.forms.register_form import RegisterForm


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")

    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect("/dashboard")

    try:
        return render_template("views/auth/login.html", form=form)
    except TemplateNotFound:
        abort(404)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/dashboard")

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = form.create_user()
            login_user(user)
            return redirect("/dashboard")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get("error", {})
            form.stripeToken.errors.append("We could not process your information. {}".format(err.get("message")))
        except stripe.error.RateLimitError as e:
            form.stripeToken.errors.append(
                "We cannot currently access out payment provider. Try again soon or reach out to the support team."
            )
        except stripe.error.InvalidRequestError as e:
            form.stripeToken.errors.append(
                "We cannot currently access out payment provider. Try again soon or reach out to the support team."
            )
        except stripe.error.AuthenticationError as e:
            form.stripeToken.errors.append(
                "We cannot currently access out payment provider. Try again soon or reach out to the support team."
            )
        except stripe.error.APIConnectionError as e:
            form.stripeToken.errors.append(
                "We cannot currently access out payment provider. Try again soon or reach out to the support team."
            )
        except stripe.error.StripeError as e:
            form.stripeToken.errors.append("There was a problem with the payment information.")

    try:
        return render_template("views/auth/register.html", form=form)
    except TemplateNotFound:
        abort(404)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
