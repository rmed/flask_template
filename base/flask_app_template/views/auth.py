# -*- coding: utf-8 -*-

"""This file contains authentication-related views."""

import datetime

from flask import Blueprint, current_app, flash, redirect, render_template, \
    request, url_for
from flask_babel import _
from flask_login import confirm_login, current_user, login_user, logout_user, \
    login_required
from passlib import pwd
from sqlalchemy import or_

from flask_app_template import db, crypto_manager
from flask_app_template.forms import LoginForm, ForgotPasswordForm, \
    ReauthenticationForm, PasswordResetForm
from flask_app_template.models import User
from flask_app_template.util import is_safe_url, send_email


bp_auth = Blueprint('auth', __name__)


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    """Log the user in."""
    form = LoginForm()

    if form.validate_on_submit():
        # Check credentials
        user = (
            User.query
            .filter(
                or_(
                    User.username==form.identity.data,
                    User.email==form.identity.data
                )
            )
        ).first()

        if not user or not crypto_manager.verify(form.password.data, user.password):
            # Show invalid credentials message
            flash(_('Invalid credentials'), 'error')

            return render_template('auth/login.html', form=form)

        # Log the user in
        if login_user(user, remember=form.remember_me.data):
            flash(_('Logged in successfully'), 'success')

            # Validate destination
            next_url = request.args.get('next')

            if next_url and is_safe_url(next_url):
                return redirect(next_url)

            return redirect(url_for('general.home'))

        # User is not allowed
        flash(_('Invalid credentials'), 'error')

    return render_template('auth/login.html', form=form)


@bp_auth.route("/logout")
@login_required
def logout():
    """Log the user out."""
    logout_user()

    return redirect(url_for('auth.login'))


@bp_auth.route('/reauthenticate', methods=['GET', 'POST'])
@login_required
def reauthenticate():
    """Ask the user to confirm their password."""
    form = ReauthenticationForm()

    if form.validate_on_submit():
        # Check credentials
        if crypto_manager.verify(form.password.data, current_user.password):
            # Show invalid credentials message
            flash(_('Invalid credentials'), 'error')

            return render_template('auth/reauthenticate.html', form=form)

        # Refresh session
        confirm_login()

        #TODO validate redirect
        return redirect(form.next.data)

    return render_template('auth/reauthenticate.html', form=form)


@bp_auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Show a form to request a password reset token.

    This does not tell the user whether the emails is valid or not. In
    addition, if the user already had a password reset token, it will be
    overwritten.
    """
    if current_user.is_authenticated:
        # Authenticated user cannot do this
        logout_user()

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        # Verify user (must be active)
        user = (
            User.query
            .filter_by(email=form.email.data)
            .filter_by(is_active=True)
        ).first()

        if not user:
            # Don't let the user know
            flash(_('A password reset token has been sent'), 'success')
            return render_template('auth/forgot_password.html', form=form)

        # Set token
        token = pwd.genword(entropy='strong', length=100, charset='hex')

        user.password_reset_token = token
        user.reset_expiration = (
            datetime.datetime.utcnow() + datetime.timedelta(days=1)
        )

        try:
            correct = True
            db.session.commit()

            # Send notification email
            send_email(
                _('Password reset'),
                recipients=[user.email],
                body=render_template(
                    'email/auth/forgot_password.txt',
                    token=token
                )
            )

            flash(_('A password reset token has been sent'), 'success')
            return render_template('auth/forgot_password.html', form=form)

        except Exception:
            correct = False
            current_app.logger.exception(
                'Failed to update password reset token for %s' % user.username
            )

            # Don't let the user know
            flash(_('A password reset token has been sent'), 'success')
            return render_template('auth/forgot_password.html', form=form)

        finally:
            if not correct:
                db.session.rollback()

    return render_template('auth/forgot_password.html', form=form)


@bp_auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Show a form to reset account password.

    Args:
        token (str): Random token mailed to the user.
    """
    if current_user.is_authenticated:
        # Authenticated user cannot do this
        logout_user()

    # Verify token
    now = datetime.datetime.utcnow()
    user = (
        User.query
        .filter_by(reset_password_token=token)
        .filter_by(is_active=True)
        .filter(User.reset_expiration >= now)
    ).first()

    if not user:
        flash(_('Invalid password reset token provided'), 'error')
        return redirect(url_for('auth.login'))

    # Show form
    form = PasswordResetForm()

    if form.validate_on_submit():
        # Update user
        user.password = crypto_manager.hash(form.password.data)

        try:
            correct = True
            db.session.commit()

            # Send notification email
            send_email(
                _('Password reset notification'),
                recipients=[user.email],
                body=render_template('email/auth/password_changed.txt')
            )

            flash(_('Password updated, you may now login'), 'success')
            return redirect(url_for('auth.login'))

        except Exception:
            correct = False
            current_app.logger.exception('Failed to reset user password')

            flash(_('Error updating password, contact an admin'), 'error')
            return render_template('auth/reset_password.html', form=form)

        finally:
            if not correct:
                db.session.rollback()

    return render_template('auth/reset_password.html', form=form)
