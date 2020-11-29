FROM python:3.9-slim-buster

RUN mkdir -p /mystripeapp
RUN touch /var/log/mystripeapp.log

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libmariadbclient-dev tzdata build-essential

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

COPY . /mystripeapp
WORKDIR /mystripeapp

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -e .

ENTRYPOINT ["gunicorn"]
CMD ["-w", "4", "--capture-output", "--log-level=debug", "--reload", "-b", "0.0.0.0:5000", "mystripeapp.bootstrap:app"]
