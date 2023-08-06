autoguard
=========

The ``autoguard`` project enables a Sentry server to use REMOTE_USER authentication.

It's mostly a special sentry configuration file, modified to hook authentication
backends and Django middlewares to the proper RemoteUser classes.

It also uses getconf_ to read settings from INI configuration files.


Usage
-----

The ``autoguard`` configuration can be tuned in a few ways:

* Specific environment variables (starting with ``AUTOGUARD_``)
* Reading from ``/etc/autoguard/settings/*.ini``
* On a dev checkout, reading from ``/path/to/autoguard_checkout/local_settings.ini``

All options are described in ``autoguard/example_settings.ini`` file.

Use autoguard almost as you would use Sentry. It auto-discovers the ``sentry_conf.py`` config file::

    autoguard start

If using the docker image build by the attached Dockerfile. The entrypoint is the "autoguard" command::

    docker run --name redis redis:latest
    docker run <IMAGE_ID> --link redis:redis --volume <CONFIG_DIR>:/etc/autoguard start


Security
--------

Autoguard expects to run behind a **HTTPS** reverse proxy; that proxy *MUST* set the ``X-Forwarded-Proto`` HTTP header
to ``https`` for HTTPS requests.

The authentication is based on ``X-Remote-User`` HTTP header, the proxy *MUST* clean it before passing to the application.


.. _getconf: https://github.com/polyconseil/getconf
