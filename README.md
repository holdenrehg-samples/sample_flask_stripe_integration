# mystripeapp

Sample Flask + Stripe application.

[Tutorial and explanation written up on medium.](https://medium.com/@reedrehg/a-flask-stripe-saas-template-cab289c11316)

---

## Getting setup

### 1. Update your hosts file

Update your `/etc/hosts` file by adding the following line:

```sh
0.0.0.0 mystripeapp.local
```

### 2. Get the code

Clone down the repository.

**The details in this readme are assuming you clone down the repo as `mystripeapp` so you may experience issues or have to slightly alter commands if you clone it down as another directory name.**

```sh
$ git clone https://github.com/holdenrehg/sample_flask_stripe_integration mystripeapp
```

### 3. Update the environment variables

There is a set of environment variables located under `mystripeapp/utils/__init__.py` that need to be updated before running the application

The only two environment variables that you should need to change to get the application up and running are the stripe token and the stripe product code.

```python
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
```

It's also information for you to add your public stripe key to the javascript on the register form. See the `mystripeapp/ui/views/auth/register.html` file.

```javascript
// Create a Stripe client.
var stripe = Stripe('****');
```

---

## Running the application

## Start the application

```sh
$ cd mystripeapp
$ docker-compose up
```

### Migrate the database

Make sure to leave the application running before migrating the database:

```sh
$ docker-compose exec app flask db upgrade
```

### Access the application

You'll be able to access at http://mystripeapp.local:5200 .

---

## Testing the application manually

You can create an account using fake Stripe cards found at https://stripe.com/docs/testing . Use these on the http://mystripeapp.local:5200/register registration form.

## Running automated tests

```sh
$ python3 setup.py test --container $(docker ps -q --filter name=mystripeapp_app)
$ python3 setup.py test --container $(docker ps -q --filter name=mystripeapp_app) --no-coverage
```

## Useful commands

Since we are running the application with docker, here are some useful commands to know:

```sh
# Run a command inside of the app container
$ docker exec -it $(docker ps -q --filter=mystripeapp_app) {command}

$ docker exec -it $(docker ps -q --filter=mystripeapp_app) ipython3
$ docker exec -it $(docker ps -q --filter=mystripeapp_app) bash
$ docker exec -it $(docker ps -q --filter=mystripeapp_app) flask init db
```

While developing you'll often need some simple knowledge of the docker-compose commands such as:

```sh
$ docker-compose stop
$ docker-compose restart
```
