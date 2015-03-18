from flask import Blueprint, render_template
from ..models import Example

example = Blueprint('example', __name__)

@example.route('/')
def index():
    return render_template('example.index.html')
