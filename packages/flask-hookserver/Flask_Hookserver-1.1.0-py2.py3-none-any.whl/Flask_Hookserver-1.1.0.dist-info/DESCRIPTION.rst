Flask-Hookserver
================

.. image:: https://img.shields.io/travis/nickfrostatx/flask-hookserver.svg
    :target: https://travis-ci.org/nickfrostatx/flask-hookserver

.. image:: https://img.shields.io/coveralls/nickfrostatx/flask-hookserver.svg
    :target: https://coveralls.io/github/nickfrostatx/flask-hookserver

.. image:: https://img.shields.io/pypi/v/flask-hookserver.svg
    :target: https://pypi.python.org/pypi/flask-hookserver

.. image:: https://img.shields.io/pypi/l/flask-hookserver.svg
    :target: https://raw.githubusercontent.com/nickfrostatx/flask-hookserver/master/LICENSE

GitHub webhooks using Flask.

This tool receives webhooks from GitHub and passes the data along to a
user-defined function. It validates the HMAC signature, and checks that the
originating IP address comes from the GitHub IP block.

Supports Flask >= 0.9

Installation
------------

.. code-block:: bash

    $ pip install Flask-Hookserver

Usage
-----

.. code-block:: python

    from flask import Flask
    from flask.ext.hookserver import Hooks

    app = Flask(__name__)
    app.config['GITHUB_WEBHOOKS_KEY'] = 'my_secret_key'

    hooks = Hooks(app, url='/hooks')

    @hooks.hook('ping')
    def ping(data, guid):
        return 'pong'

    app.run()

And there we go! ``localhost:8000/hooks`` will now accept GitHub webhook
events.

Config
------

Signature and IP validation are both optional, but turned on by default.  They
can each be turned off with a config flag.

.. code-block:: python

    app = HookServer(__name__)
    app.config['VALIDATE_IP'] = False
    app.config['VALIDATE_SIGNATURE'] = False

If ``VALIDATE_SIGNATURE`` is set to ``True``, you need to supply the secret key
in ``app.config['GITHUB_WEBHOOKS_KEY']``.

Exceptions
----------

If anything goes wrong, a regular ``HTTPException`` will be raised. Possible
errors include:

- 400: Some headers are missing
- 400: The request body isn't valid JSON
- 400: The signature is missing or incorrect
- 403: The request originated from an invalid IP address
- 503: Could not download the valid webhooks IP block from GitHub


.. :changelog:

History
-------

1.1.0 (2016-04-10)
++++++++++++++++++

- Use GITHUB_WEBHOOKS_KEY if provided, fallback on SECRET_KEY

1.0.0 (2015-12-25)
++++++++++++++++++

- Refactor into a proper Flask extension
- Move from hookserver to flask.ext.hookserver
- Introduce a single hooks object that can be registered to multiple apps
- Remove importable blueprint and standalone Flask app
- Rename KEY to GITHUB_WEBHOOKS_KEY

0.3.2 (2015-11-28)
++++++++++++++++++

- Don't actually connect to GitHub from test suite
- Deploy to PyPI from Travis

0.3.1 (2015-11-19)
++++++++++++++++++

- Accept unicode keys
- Default to true for VALIDATE_IP and VALIDATE_SIGNATURE if missing

0.3.0 (2015-11-08)
++++++++++++++++++

- Move hooks URL route into a blueprint
- Report rate limit expire time when the GitHub request limit is exceeded

0.2.1 (2015-10-21)
++++++++++++++++++

- Install Requests security dependencies

0.2.0 (2015-10-21)
++++++++++++++++++

- Proper Python 2.7 support
- Respect GitHub rate limit of 60 requests per hour
- Make key param to HookServer optional
- Add optional param url
- Use VALIDATE_IP and VALIDATE_SIGNATURE instead of DEBUG
- Simplify some error messages
- Add test suite

0.1.4 (2015-04-07)
++++++++++++++++++

- Support IPv4 addresses mapped to IPv6

0.1.3 (2014-07-10)
++++++++++++++++++

- Fix Python 2 bug in IP address decoding

0.1.2 (2014-07-09)
++++++++++++++++++

- Ignore HMAC in debug mode

0.1.1 (2014-07-08)
++++++++++++++++++

- Reload GitHub IP block on each request

0.1.0 (2014-07-07)
++++++++++++++++++

- Initial release


