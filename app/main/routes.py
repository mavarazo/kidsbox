from flask import render_template

from app.main import bp
from app.models import Tag


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home', tags=Tag.query.filter(Tag.path!=None).all())

