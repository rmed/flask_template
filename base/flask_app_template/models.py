# -*- coding: utf-8 -*-

"""This file contains SQLAlchemy model declarations."""

import datetime
import os

from flask_user import UserMixin
from sqlalchemy import event
from sqlalchemy.ext.associationproxy import association_proxy

from flask_app_template import db


# Flask-User models
class Role(db.Model):
    """Flask-User model for user roles.

    Attributes:
        id (int): Unique ID of the role.
        name (str): Unique name of the role.
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    @classmethod
    def get_role(self, name):
        """Obtain an already existing role by name.

        Args:
            name (str): Unique name of the role.

        Returns:
            Role instance or None if not found.
        """
        role = Role.query.filter_by(name=name).first()

        return role


class User(db.Model, UserMixin):
    """Flask-User model for users.

    Includes additional attributes.

    Attributes:
        locale (str): Locale code.
        timezone (str): Timezone used to localize dates.
        has_image (bool): Whether the user has uploaded a profile image.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime)

    # User information
    is_enabled = db.Column(db.Boolean, nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    # Additional attributes
    locale = db.Column(db.String(2), nullable=False, default='en')
    timezone = db.Column(db.String(50), nullable=False, default='UTC')

    # Relationships
    roles = db.relationship(
        'Role', secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'),
        cascade='delete, save-update', collection_class=set
    )

    # Proxies
    role_names = association_proxy(
        'roles',
        'name',
        creator=lambda n: Role.get_role(n)
    )

    def is_active(self):
        return self.is_enabled

    @classmethod
    def get_by_username(self, username):
        """Obtain an already existing user by username.

        Args:
            username (str): Unique username of the user

        Returns:
            User instance or None if not found.
        """
        user = User.query.filter_by(username=username).first()

        return user


class UserRoles(db.Model):
    """Flask-User model for user-role relations."""
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE')
    )
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id', onupdate='CASCADE', ondelete='CASCADE')
    )
