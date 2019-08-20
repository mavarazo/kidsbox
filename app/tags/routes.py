from flask import render_template, request, abort

from app import db
from app.models import Tag
from app.schemas import tag_schema
from app.tags import bp


@bp.route('/tags', methods=['GET'])
@bp.route('/tags/index', methods=['GET'])
def index():
    return render_template('tags/index.html', title='Tags', tags=Tag.query.all())


@bp.route('/tags/api/<uid>', methods=['GET'])
def find_by_uid(uid):
    tag = Tag.query.filter_by(uid=uid).first_or_404()
    return tag_schema.jsonify(tag)


@bp.route('/tags/api/', methods=['POST'])
def store_uid():
    if not request.json or 'uid' not in request.json:
        abort(400)

    tag = Tag(uid=request.json.get('uid'))
    db.session.add(tag)
    db.session.commit()
    return tag_schema.jsonify(tag)

