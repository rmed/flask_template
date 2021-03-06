# -*- coding: utf-8 -*-

"""This file contains utility code."""

from urllib.parse import urlparse, urljoin

from flask import request
from flask_mail import Message


class CryptoManager(object):
    """Wrapper for passlib cryptography.

    The manager expects the following configuration variables:

    - `PASSLIB_SCHEMES`: List of passlib hashes for the underlying
        `CryptoContext` object. If a string is provided, it should be a
        comma-separated list of hashes supported by `passlib`. Defaults to
        `'bcrypt'`.
    - `PASSLIB_DEPRECATED`: List of passlib hashes that are deprecated
        (defaults to `"auto"`, which will deprecate all hashes except
        for the first hash type present in the `PASSLIB_SCHEMES` configuration
        variable). If a string different from `"auto"` is provided, it should
        be a comma-separated list of hashes supported by `passlib`. Defaults
        to an empty list.

    Moreover, the manager offers a direct translation of optional algorithm options for
    the underlying context (see
    <https://passlib.readthedocs.io/en/stable/lib/passlib.context.html#algorithm-options>).
    These are in the form `PASSLIB_ALG_<SCHEME>_<CONFIG>` and will be translated to the
    appropriate `<scheme>__<config>` configuration variable name internally.
    """

    def __init__(self):
        self._context = None

    def __getattr__(self, attr):
        """Wrap the internal passlib context."""
        if attr in ('init_app', '_context'):
            return getattr(self, attr)

        # Calling hasher methods
        return getattr(self._context, attr)

    def init_app(self, app):
        """Initialize manager.

        Args:
            app: Application instance

        Raises:
            `ModuleNotFoundError` in case `passlib` is not installed or
            `KeyError` if a configuration variable is missing.
        """
        from passlib.context import CryptContext

        schemes = app.config.get('PASSLIB_SCHEMES', 'bcrypt')
        deprecated = app.config.get('PASSLIB_DEPRECATED', 'auto')

        if isinstance(schemes, str):
            schemes = [s.strip() for s in schemes.split(',')]

        if isinstance(deprecated, str):
            deprecated = [d.strip() for d in deprecated.split(',')]

        params = {
            'schemes': schemes,
            'deprecated': deprecated,
        }

        # Set algorithm options
        for key in [k for k in app.config if k.startswith('PASSLIB_ALG_')]:
            value = app.config[key]
            scheme, option = key.replace('PASSLIB_ALG_', '').lower().split('_', 1)

            params['{}__{}'.format(scheme, option)] = value

        self._context = CryptContext(**params)


class HashidsWrapper(object):
    """Wrapper for deferred initialization of Hashids.

    This is optional and can be disabled by setting the configuration
    parameter `USE_HASHIDS` to `False`.

    If used, the wrapper expects the following configuration parameters:

    - `HASHIDS_SALT`: Salt to use when hashing IDs.
    - `HASHIDS_LENGTH`: Minimum length of the hash (defaults to 8).
    """

    def __init__(self):
        self._hasher = None
        self._initialized = False

    def __getattr__(self, attr):
        """Wrap internal Hashids attributes."""
        if attr in ('init_app', '_hasher', '_initialized'):
            return getattr(self, attr)

        # Calling hasher methods
        if self._initialized:
            return getattr(self._hasher, attr)

        return getattr(self, attr)

    def decode(self, id):
        """Fallback in case the wrapper was not initialized.

        Returns:
            `None`
        """
        return None

    def encode(self, id):
        """Fallback in case the wrapper was not initialized.

        Returns:
            `None`
        """
        return None

    def init_app(self, app):
        """Create a Hashids instance for the application.

        Args:
            app: Application instance

        Raises:
            `ModuleNotFoundError` in case `hashids` is not installed or
            `KeyError` if a configuration variable is missing.
        """
        if app.config.get('USE_HASHIDS', False):
            from hashids import Hashids

            self._hasher = Hashids(
                salt=app.config['HASHIDS_SALT'],
                min_length=app.config.get('HASHIDS_LENGTH', 8)
            )

            self._initialized = True


def is_safe_url(target):
    """Check whether the target is safe for redirection.

    Args:
        target (str): Target URL/path.

    Returns:
        `True` if the URL is safe, otherwise `False`.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def send_email(*args, **kwargs):
    """Send an email.

    This function may be extended in case the Celery recipe is used
    in order to use the asynchronous email delivery.

    All arguments are passed as-is to Flask-Mail.

    Returns:
        Mail send result.
    """
    from flask_app_template import mail

    message = Message(*args, **kwargs)

    return mail.send(message)
