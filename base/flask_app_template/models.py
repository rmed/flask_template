# -*- coding: utf-8 -*-

"""This file contains SQLAlchemy model declarations."""

from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy

from flask_app_template import db, hashids_hasher


# Intermediate user-role table
user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id', name='fk_user_roles_user')
    ),
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id', name='fk_user_roles_role')
    )
)


class BaseModel(db.Model):
    """Base class used to implement common methods."""
    __abstract__ = True

    @property
    def hashid(self):
        """Obtain the HashId token on the fly."""
        return hashids_hasher.encode(self.id)

    @classmethod
    def exists(cls, id):
        """Check whether an instance exists.

        Returns:
            Boolean indicating if the instance exists.
        """
        return cls.query.filter_by(id=id).scalar()

    @classmethod
    def get_by_id(cls, id):
        """Get instance by id.

        Returns:
            Instance or `None` if not found.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_hashid(cls, token):
        """Get instance by HashId token.

        Returns:
            Instance or `None` if not found.
        """
        instance_id = hashids_hasher.decode(token)

        if not instance_id:
            return None

        return cls.query.filter_by(id=instance_id[0]).first()

    def update(self, **kwargs):
        """Update instance attributes from dictionary.

        Key and value validation should be performed beforehand!
        """
        for k, v in kwargs.items():
            setattr(self, k, v)


# Authentication/Authorization models
class Role(BaseModel):
    """Model for defining roles.

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
        return Role.query.filter_by(name=name).first()


class User(BaseModel, UserMixin):
    """User model.

    Attributes:
        username (str): Unique username.
        password (str): Password hash.
        reset_password_token (str): Token used to reset user password.
        email (str): Email of the user.
        is_active (bool): Whether the user is active in the application.
        locale (str): Locale code.
        timezone (str): Timezone used to localize dates.
        roles (set(Role)): Roles assigned to the user.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=True)
    reset_expiration = db.Column(db.DateTime(), nullable=True)

    # Email information
    email = db.Column(db.String(255), nullable=False, unique=True)

    # User information
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    locale = db.Column(db.String(12), nullable=False, default='en')
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

    @classmethod
    def get_by_username(self, username):
        """Obtain an already existing user by username.

        Args:
            username (str): Unique username of the user

        Returns:
            User instance or `None` if not found.
        """
        return User.query.filter_by(username=username).first()