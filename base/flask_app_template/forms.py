# -*- coding: utf-8 -*-

"""This file contains form definitions."""

from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms import validators


class LoginForm(FlaskForm):
    """Application login form."""
    identity = StringField(
        _l('Username or email'),
        validators=[
            validators.DataRequired(_l('Identity is required')),
        ]
    )

    password = PasswordField(
        _l('Password'),
        validators=[
            validators.DataRequired(_l('Password is required')),
        ]
    )

    remember_me = BooleanField(_l('Remember me'))

    submit = SubmitField(_l('Sign in'))


class ForgotPasswordForm(FlaskForm):
    """Form to request password reset token."""
    email = StringField(
        _l('Email'),
        validators=[
            validators.DataRequired(_l('Email is required')),
            validators.Email(_l('Invalid Email'))
        ]
    )

    submit = SubmitField(_l('Reset password'))


class ReauthenticationForm(FlaskForm):
    """Reauthentication form."""
    password = PasswordField(
        _l('Password'),
        validators=[
            validators.DataRequired(_l('Password is required')),
        ]
    )

    submit = SubmitField(_l('Sign in'))


class PasswordResetForm(FlaskForm):
    """Reset password form."""
    password = PasswordField(
        _l('New password'),
        validators=[validators.DataRequired(_l('Password is required'))]
    )

    retype_password = PasswordField(
        _l('Retype new password'),
        validators=[
            validators.EqualTo(
                'password',
                message=_l('Passwords did not match')
            )
        ]
    )

    submit = SubmitField(_l('Reset password'))
