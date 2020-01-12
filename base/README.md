# Flask application template

This is the *basic* application template, including:


- Basic authentication and authorization through [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Hashids](https://hashids.org/) support (see the `hashids_hasher` object in `flask_app_template/__init__.py`
- Localization support per user, including timezones
- Database migrations ([Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/))
- CSRF protection for AJAX calls
- Markdown support ([Flask-Misaka](https://flask-misaka.readthedocs.io/en/latest/))
- Datetime filter for Jinja templates (see `format_datetime` function)
- Several assets (managed through [Flask-Assets](https://flask-assets.readthedocs.io/en/latest/))
    - [Bulma](https://bulma.io) styles (+ some extensions)
    - [Zepto.js](https://zeptojs.com/)
    - [Font Awesome](https://fontawesome.com/)
    - Custom Javascript functions for navigation purposes
    - `libsass` used to compile SASS assets
- Default basic and development configurations (see `bootstrap.py`)
- Default layout
- Custom macros (**render form fields**, **render pagination controls**, etc.)
- Several commands (user management, translation)
- A default `setup.py` file


## Usage

Download or clone the repository and replace `flask_app_template` with the name of your application. For example, you could replace the term using the following command in this directory:

```
egrep -lRZ 'flask_app_template' . | xargs -0 -l sed -i -e 's/flask_app_template/myApp/g'
```

The install the requirements through `pip` (`virtualenv` is recommended):

```
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

**Production configuration is set through the `FLASK_APP_CONFIG` environment variable.** 

## CSRF

By default, all AJAX requests that could modify data (`POST`, `PUT`, etc.) are protected with a CSRF token when the document is loaded. This token is conditionally included in the default layout as follows:

```html+jinja
{# CSRF token. Set flag in templates when needed #}
{% if _include_csrf %}
    <meta name="csrf-token" content="{{ csrf_token() }}"/>
{% endif %}
```

In order to enable the token, simply extend the layout in a template and set the value of `_include_csrf`:

```html+jinja
{% extends "layout.html" %}

{% set _include_csrf = true %}

{% block content %}
    Content here....
{% endblock %}
```

## Configuration

Apart from the configuration variables defined by each of the extensions used, the template includes the following additional variables:

### Passlib

- `PASSLIB_SCHEMES`: List of passlib hashes for the underlying `CryptoContext` object. If a string is provided, it should be a comma-separated list of hashes supported by `passlib`. Defaults to `'bcrypt'`.
- `PASSLIB_DEPRECATED`: List of passlib hashes that are deprecated (defaults to `"auto"`, which will deprecate all hashes except for the first hash type present in the `PASSLIB_SCHEMES` configuration variable). If a string different from `"auto"` is provided, it should be a comma-separated list of hashes supported by `passlib`. Defaults to an empty list.

Moreover, the manager offers a direct translation of optional algorithm options for the underlying context (see <https://passlib.readthedocs.io/en/stable/lib/passlib.context.html#algorithm-options>). These are in the form `PASSLIB_ALG_<SCHEME>_<CONFIG>` and will be translated to the appropriate `<scheme>__<config>` configuration variable name internally.

**Note**: If using `bcrypt` as the hashing algorithm, it is recommended to install the `bcrypt` Python library.

### Hashids

- `USE_HASHIDS`: set to `True` to enable HashIds support or to `False` to disable it. If disabled, the wrapper will return `None` whenever trying to encode/decode IDs as a fallback
- `HASHIDS_SALT` (**required**): salt to use when encoding IDs
- `HASHIDS_LENGTH`: minimum length of the hashes (defaults to 8)
