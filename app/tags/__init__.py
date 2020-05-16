from flask import Blueprint

bp = Blueprint('tags', __name__,
                template_folder='templates',
                static_folder='static')

from app.tags import routes, api