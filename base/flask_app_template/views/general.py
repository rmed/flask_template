# -*- coding: utf-8 -*-

"""This file contains general views."""


from flask import Blueprint, render_template
from flask_babel import _
from flask_user import login_required

from flask_app_template import db


bp_general = Blueprint('general', __name__)


@bp_general.route('/')
@login_required
def home():
    """Show the home of the user."""
    return render_template('general/home.html')
