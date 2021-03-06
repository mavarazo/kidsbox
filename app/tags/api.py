from flask import request, jsonify, current_app

from app import db, mpd
from app.errors.handlers import api_error_response
from app.models import Tag
from app.schemas import tag_schema
from app.tags import bp


def mpd_command(command=None, args=None):
    try:
        mpd.connect(current_app.config["MPD_HOST"], current_app.config["MPD_PORT"])
    except:
        return api_error_response(500, "could not establish connection to mpd")

    if 'play' == command:
        mpd.clear()
        mpd.add(args)
        mpd.play()
    elif 'pause' == command:
        mpd.pause()
    elif 'stop' == command:
        mpd.clear()
        mpd.stop()
    elif 'next' == command:
        mpd.next()
    elif 'prev' == command:
        mpd.previous()

    response = mpd.currentsong()

    if 'status' == command:
        response = mpd.status()

    mpd.disconnect()
    return jsonify({'status': response})


@bp.route('/tags/api/<uid>', methods=['GET'])
def find_by_uid(uid):
    tag = Tag.query.filter_by(uid=uid).first_or_404()
    return tag_schema.jsonify(tag)


@bp.route('/tags/api/', methods=['POST'])
def store_uid():
    if not request.json or 'uid' not in request.json:
        return api_error_response(400, "'UID' is mandatory")

    tag = Tag(uid=request.json.get('uid'))
    db.session.add(tag)
    db.session.commit()
    return tag_schema.jsonify(tag)


@bp.route('/tags/api/status', methods=['GET'])
def status():
    return mpd_command('status')


@bp.route('/tags/api/currentsong', methods=['GET'])
def currentsong():
    return mpd_command('currentsong')


@bp.route('/tags/api/play/<uid>', methods=['GET'])
def play_by_uid(uid):
    tag = Tag.query.filter_by(uid=uid).first_or_404()
    if tag.path is None:
        return api_error_response(400, "'" + uid + "' not assigned")

    return mpd_command('play', tag.path)


@bp.route('/tags/api/pause', methods=['GET'])
def pause():
    return mpd_command('pause')


@bp.route('/tags/api/stop', methods=['GET'])
def stop():
    return mpd_command('stop')


@bp.route('/tags/api/next', methods=['GET'])
def next():
    return mpd_command('next')


@bp.route('/tags/api/prev', methods=['GET'])
def prev():
    return mpd_command('prev')
