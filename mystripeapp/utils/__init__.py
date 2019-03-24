from . import models


def environment():
    """
    This is not how you would want to handle environments in a real project,
    but for the sake of simplicity I'll create this function.

    Look at using environment variables or dotfiles for these.
    """
    return {
        "app": {"name": "mystripeapp.local", "port": "5200", "secret": "my_super_secret_key"},
        "billing": {"stripe": {"token": "****", "product": "****"}},
        "database": {
            "provider": "mysql",
            "host": "mariadb",
            "port": "3306",
            "username": "stripeapp",
            "password": "stripeapp",
            "database": "stripeapp",
        },
    }
