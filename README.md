# mystripeapp

Sample Flask + Stripe application.

---

## Getting setup

### 1. Update your hosts file

Update your `/etc/hosts` file by adding the following line:

```
0.0.0.0 mystripeapp.local
```

### 2. Get the code

Clone down the repository.

**The details in this readme are assuming you clone down the repo as `mystripeapp` so you may experience issues or have to slightly alter commands if you clone it down as another directory name.**

```
git clone https://github.com/holdenrehg/sample_flask_stripe_integration mystripeapp
```

### 3. Update the environment variables

There is a set of environment variables located under `mystripeapp/utils/__init__.py` that need to be updated before running the application

The only two environment variables that you should need to change to get the application up and running are the stripe token and the stripe product code.

```
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

---

## Running the application

## Start the application

```
cd mystripeapp
docker-compose up -d
```

### Migrate the database

```
docker exec -it $(docker ps -q --filter name=mystripeapp_app) flask db init
docker exec -it $(docker ps -q --filter name=mystripeapp_app) flask db migrate
docker exec -it $(docker ps -q --filter name=mystripeapp_app) flask db upgrade
```

### Access the application

You'll be able to access at http://mystripeapp.local:5200 .

---

## Running the tests

```
python3 setup.py test --container $(docker ps -q --filter name=mystripeapp_app)
python3 setup.py test --container $(docker ps -q --filter name=mystripeapp_app) --no-coverage
```

## Useful commands

Since we are running the application with docker, here are some useful commands to know:

```
# Run a command inside of the app container
docker exec -it $(docker ps -q --filter=mystripeapp_app) {command}

docker exec -it $(docker ps -q --filter=mystripeapp_app) ipython3
docker exec -it $(docker ps -q --filter=mystripeapp_app) bash
docker exec -it $(docker ps -q --filter=mystripeapp_app) flask init db
```

While developing you'll often need some simple knowledge of the docker-compose commands such as:

```
docker-compose stop
docker-compose restart
```