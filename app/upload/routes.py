from flask import render_template

from app.upload import bp
from app.upload.forms import UploadForm


@bp.route('/upload', methods=['GET'])
@bp.route('/upload/index', methods=['GET'])
def index():
    return render_template('upload/index.html', title='Upload', form=UploadForm())

