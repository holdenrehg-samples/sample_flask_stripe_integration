import json

import stripe
from flask import abort, redirect, render_template
from flask_login import current_user, login_required, logout_user
from jinja2 import TemplateNotFound

from mystripeapp import utils
from mystripeapp.bootstrap import app, db


@app.route("/dashboard")
@login_required
def dashboard():
    try:
        return render_template("views/dashboard.html", user=current_user)
    except TemplateNotFound:
        abort(404)


@app.route("/account/delete", methods=["POST"])
@login_required
def delete_account():
    env = utils.environment()

    stripe.api_key = env["billing"]["stripe"]["token"]
    for subscription in stripe.Subscription.list(customer=current_user.stripe_customer_id):
        if subscription.customer == current_user.stripe_customer_id:
            subscription.delete()

    db.session.delete(current_user)
    db.session.commit()

    logout_user()
    return redirect("/")
