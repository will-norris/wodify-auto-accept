# wodify-auto-accept

SImple script for scanning your gmail inbox and automatically claiming spots in wodify waitlist notification emails

## Requirements
Python 3.8 + Gmail credentials - The script itself can either be run in a docker container or on its own on your local machine


## Running without docker

Create a Python 3.8 virtualenv and then install the required packages using pip. From the project root run:

```bash
virtualenv venv -p python3.8
source ./venv/bin/activate
pip install -r requirements.txt
python ./src/app.py
```

## Running with docker

The repo contains a docker-compose file so getting the script up and running is easy

```bash
docker-compose up -d app
```

## Running on remote hosts
This can be done pretty easily using docker contexts. For example, I run this script at home on a raspberry pi using the following configuration:

First, add an entry to your ssh config if you don't already have it for your remote machine:

```bash
Host pi
 Hostname 192.168.0.39
 User pi
 IdentityFile ~/.ssh/pi_key
```

Next, create a docker context which uses this ssh config entry - note: the ssh://pi name should match the `Host` name from the ssh config

```bash
docker context create pi --description "Raspberry pi host" --docker "host=ssh://pi"
```

Finally tell docker to use this context when executing commands:

```bash
docker context use pi
```

Any docker commands you run from this point onwards will be run against the installation of docker on the raspberry pi.