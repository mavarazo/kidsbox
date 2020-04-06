from flask import render_template, send_from_directory, current_app

from app.main import bp
from app.models import Tag


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home', tags=Tag.query.filter(Tag.path!=None).order_by(Tag.name).all())


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

