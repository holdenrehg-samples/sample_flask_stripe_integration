from flask import abort, render_template
from jinja2 import TemplateNotFound

from mystripeapp.bootstrap import app


@app.route("/")
def welcome():
    try:
        return render_template("views/landing.html")
    except TemplateNotFound:
        abort(404)
