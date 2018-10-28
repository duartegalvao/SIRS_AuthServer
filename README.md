# SIRS Authentication Server

## Description

SIRS project authentication server (+ web app) component.

## Instructions

### Set-up

After cloning the project, you should create a virtual-env in the root folder, as follows:

```bash
virtualenv -p python3 auth-env
```

### Running

Make sure you are inside the environment:

```bash
source auth-env/bin/activate
```

Your shell prompt should have "`(auth-env)`" in the beginning.

Then, make sure all of the project requirements are installed:

```bash
pip3 install -r requirements.txt
```

After that you can just run the test-server:

```bash
python3 auth/manage.py runserver
```

### Developing

Django documentation is available [here](https://docs.djangoproject.com/en/2.1/).

### Exiting

To leave the environment, run:

```bash
deactivate
```

## Team

| Number | Name             |
| ------ | ---------------- |
| 83422  | Amândio Faustino |
| 83449  | Duarte Galvão    |
| 83524  | Marta Cruz       |
