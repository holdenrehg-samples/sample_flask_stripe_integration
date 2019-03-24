from mystripeapp.bootstrap import app
from flask import render_template, abort
from jinja2 import TemplateNotFound


@app.route("/")
def welcome():
    """
    Show the landing page.
    """
    try:
        return render_template("views/landing.html")
    except TemplateNotFound:
        abort(404)
