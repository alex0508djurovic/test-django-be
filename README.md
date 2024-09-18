# Project Name
Django API with Caching and Swagger Documentation

# Overview
We have three API endpoints.
- `http://127.0.0.1:8000/swagger` Swagger documentation.
- `http://127.0.0.1:8000/api/search` Receives a POST request with search type(users or repositories or issues) &
search text
- `http://127.0.0.1:8000/api/search` Clear Backend Caching

## Prerequisites
Before running the server, ensure the following are installed on your system:
- [Python 3.12+](https://www.python.org/downloads/)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- Django 4.0+
- Django REST Framework
- `drf-yasg` for Swagger documentation
- `requests` library for making GitHub API calls

## Install `pipenv`
## Clone the repository **:
## Install `pipenv` if not already installed
```bash
    pip install pipenv
```
## Create a virtual environment and install dependencies
```bash
    pipenv install
```
## Run server
```bash
    python manage.py migrate
    python manage.py runserver

```