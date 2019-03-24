from mystripeapp import models
from mystripeapp.bootstrap import app


@app.login_manager.user_loader
def load_user(user_id):
    """
    Load the currently authenticated user.

    :return {User|None}:
        This will return the user object if one is found, otherwise will return
        None. It is important that this function does not raise an exception.
    """
    member = models.User.query.get(user_id)
    if member:
        return member
    return None
