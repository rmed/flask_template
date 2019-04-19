# -*- coding: utf-8 -*-

"""This file contains custom error handlers."""

from flask import Flask, render_template


def forbidden(e):
    return render_template('errors/403.html'), 403


def page_not_found(e):
    return render_template('errors/404.html'), 404


def server_error(e):
    return render_template('errors/500.html'), 500
