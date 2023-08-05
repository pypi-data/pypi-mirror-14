django-rest-sessions
=======================
Rest based sessions backend for Django.

Prerequisites
-------------
This backend relies on `rest-sessions`_ for storing and managing sessions.
Npm rest-sessions needs to be running and accessible at SESSION_URL.

.. _rest-sessions: https://www.npmjs.com/package/rest-sessions

Requirements
------------
This package relies on the `requests`_ package. Make sure it is installed in your Django project:
    ``pip install requests``

.. _requests: https://github.com/kennethreitz/requests

Install
-------
Install with pip:
    ``pip install django-rest-sessions``

Configure
---------
After installing django-rest-sessions you must add a few settings to your
settings.py

* Add ``rest_sessions`` as your session engine::

    SESSION_ENGINE = 'rest_sessions'

* Add ``django.contrib.sessions.middleware.SessionMiddleware`` to
  MIDDLEWARE_CLASSES
* Add the name of the session cookie for Django's session middleware::

    SESSION_COOKIE_NAME = 'session-cookie'

* Add the path where npm rest-sessions is running::

    SESSION_URL = 'example.com/path/to/rest-sessions'

* Add the app that is used in npm rest-sessions::

    SESSION_APP = 'mywebapp'

Usage
-----
This session backend is mostly intended to be used in a microservice
architecture and thus does not handle creating sessions since npm rest-sessions
requires a user key so it would only be possible to create a session within
the microservice that takes care of the users for your application.
Because this is intended to add sessions to requests to all microservices
written in Django it is more applicable to create sessions once a user logs in
or requests a web page and use this for services handling RESTful requests that
said web page makes.

Testing
-------
To run tests the following packages are needed:

    * django

    * requests

    * requests_mock

Install them with:
    `pip install -r requirements.txt`

Run the tests with:
    `python setup.py test` or
    `python setup.py xml_test` which generates an xml report
