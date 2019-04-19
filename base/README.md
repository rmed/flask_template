# Flask application template

This is the *basic* application template, including:


- Basic [Flask-User](https://flask-user.readthedocs.io/en/v0.6/) database models
- [Hashids](https://hashids.org/) support (see the `hashids_hasher` object in `flask_app_template/__init__.py`
- Localization support per user, including timezones
- Database migrations ([Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/))
    - A default migration with implemented `Flask-User` models is provided
- CSRF protection for AJAX calls
- Markdown support ([Flask-Misaka](https://flask-misaka.readthedocs.io/en/latest/))
- Datetime filter for Jinja templates (see `format_datetime` function)
- Several assets (managed through [Flask-Assets](https://flask-assets.readthedocs.io/en/latest/))
    - [Bulma](https://bulma.io) styles (+ some extensions)
    - [Zepto.js](https://zeptojs.com/)
    - [Font Awesome](https://fontawesome.com/)
    - Custom Javascript functions for navigation purposes
    - `libsass` used to compile SASS assets
- Default basic configuration (see `bootstrap.py`)
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
