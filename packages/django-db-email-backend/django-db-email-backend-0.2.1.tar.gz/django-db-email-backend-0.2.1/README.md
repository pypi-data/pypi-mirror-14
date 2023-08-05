Django DB Email Backend
=======================

[![Build Status](https://travis-ci.org/jsatt/django-db-email-backend.svg?branch=master)](https://travis-ci.org/jsatt/django-db-email-backend)

Django email backend for storing messages to a database. This is intended to be used in developement in cases where you want to test sending emails, but don't want to send real emails and don't have access to the console output (such as on a remote server).

This is NOT intended for production use in any capacity.

To install:

```sh
pip install django-db-email-backend
```

In settings.py:

```python
INSTALLED_APPS = [
    ...
    'db_email_backend',
]

EMAIL_BACKEND = 'db_email_backend.backend.DBEmailBackend'
```
