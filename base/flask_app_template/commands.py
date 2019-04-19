# -*- coding: utf-8 -*-

"""This file contains custom CLI commands."""

import datetime
import os

from flask.cli import FlaskGroup

from flask_app_template import db, user_manager, init_app
from flask_app_template.models import Role, User

import click


def init_wrapper(info):
    """Wrapper for the application initialization function."""
    return init_app()


@click.group(cls=FlaskGroup, create_app=init_wrapper)
def cli():
    """Management script."""
    pass


# Begin user commands
@cli.group()
def user():
    """User related commands."""
    pass


@user.command()
@click.argument('username')
@click.argument('role')
def addrole(username, role):
    """Add a role to a given user.

    \b
    Args:
        username: the username to add the role to
        role: role name
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        click.echo('User does not exist')
        return

    if role in user.role_names:
        click.echo('User already has that role')
        return


    role_exists = Role.query.filter_by(name=role).count() > 0

    if not role_exists:
        click.echo('Role does not exist')
        return

    # Update roles
    roles = [r for r in user.role_names]
    roles.append(role)

    user.role_names = set(roles)

    try:
        correct = True
        db.session.commit()

    except Exception as e:
        # Catch anything unknown
        correct = False
        click.echo(e)

    finally:
        if not correct:
            # Cleanup and show error
            db.session.rollback()
            click.echo('Error updating roles')

        else:
            click.echo('Roles updated')


@user.command()
@click.option('--username', help='username (must be unique)', prompt=True)
@click.option('--email', help='email (must be unique)', prompt=True)
@click.option('--password', help='password', prompt=True, hide_input=True)
def create(username, email, password):
    """Add a new user to the database."""
    hashed_password = user_manager.hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        confirmed_at=datetime.datetime.utcnow(),
        is_enabled=True,
    )

    try:
        correct = True
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        # Catch anything unknown
        correct = False
        click.echo(e)

    finally:
        if not correct:
            # Cleanup and show error
            db.session.rollback()

            click.echo(
                'Error creating user, make sure username and email are unique'
            )

        else:
            click.echo('New user created')


@user.command()
@click.argument('username')
def disable(username):
    """Disable a user account.

    \b
    Args:
        username: the username to disable
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        click.echo('User does not exist')
        return

    if user.is_enabled:
        click.echo('User is already enabled')
        return

    user.is_enabled = False
    user.confirmed_at = None

    try:
        correct = True
        db.session.commit()

    except Exception as e:
        # Catch anything unknown
        correct = False
        click.echo(e)

    finally:
        if not correct:
            # Cleanup and show error
            db.session.rollback()
            click.echo('Error disabling user')

        else:
            click.echo('User disabled')


@user.command()
@click.argument('username')
def enable(username):
    """Enable a user account.

    \b
    Args:
        username: the username to enable
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        click.echo('User does not exist')
        return

    if user.is_enabled:
        click.echo('User is already enabled')
        return

    user.is_enabled = True
    if not user.confirmed_at:
        user.confirmed_at = datetime.datetime.utcnow()

    try:
        correct = True
        db.session.commit()

    except Exception as e:
        # Catch anything unknown
        correct = False
        click.echo(e)

    finally:
        if not correct:
            # Cleanup and show error
            db.session.rollback()
            click.echo('Error enabling user')

        else:
            click.echo('User enabled')


@user.command()
@click.argument('username')
@click.option('--password', help='password', prompt=True, hide_input=True)
def password(username, password):
    """Change the password of a user.

    \b
    Args:
        username: user to change password for
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        click.echo('User does not exist')
        return

    hashed_password = user_manager.hash_password(password)
    user.password = hashed_password

    try:
        correct = True
        db.session.commit()

    except Exception as e:
        # Catch anything unknown
        correct = False
        click.echo(e)

    finally:
        if not correct:
            # Cleanup and show error
            db.session.rollback()

            click.echo('Failed to change password')

        else:
            click.echo('Password changed')


@user.command()
@click.argument('username')
def roles(username):
    """Show roles of a given user.

    \b
    Args:
        username: the username to list roles for
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        click.echo('User does not exist')
        return

    roles = ', '.join(user.role_names) or 'No roles'

    click.echo('Roles of user "%s": %s' % (username, roles))


# Begin translation commands
@cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
def compile():
    """Compile all languages."""
    compile_cmd = (
        'pybabel compile '
        '-d flask_app_template/translations'
    )

    if os.system(compile_cmd):
        raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    extract_cmd = (
        'pybabel extract '
        '-F babel.cfg '
        '-k "lazy_gettext _l" '
        '-o flask_app_template/translations/messages.pot .'
    )

    init_cmd = (
        'pybabel init '
        '-i flask_app_template/translations/messages.pot '
        '-d flask_app_template/translations '
        '-l {}'
    )

    if os.system(extract_cmd):
        raise RuntimeError('extract command failed')

    if os.system(init_cmd.format(lang)):
        raise RuntimeError('init command failed')


@translate.command()
def update():
    """Update message catalog."""
    extract_cmd = (
        'pybabel extract '
        '-F babel.cfg '
        '-k "lazy_gettext _l" '
        '-o flask_app_template/translations/messages.pot .'
    )

    update_cmd = (
        'pybabel update '
        '-i flask_app_template/translations/messages.pot '
        '-d flask_app_template/translations'
    )


    if os.system(extract_cmd):
        raise RuntimeError('extract command failed')

    if os.system(update_cmd):
        raise RuntimeError('update command failed')


if __name__ == '__main__':
    cli()
