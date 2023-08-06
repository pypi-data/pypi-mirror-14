==========
django-uri
==========

Installation
============

::

    pip install django-uri


Usage
=====

::

    request.uri.origin
    request.uri.scheme


Settings.py
===========

::

    MIDDLEWARE_CLASSES = (
        ...
        'detect.middleware.UserAgentDetectionMiddleware',
        ...
    )

    USER_AGENT_DETECTION = (
        # Regex have at most one parentheses
        # ('key1', r'regex1'),
        # ('key2', r'regex2'),
    )

