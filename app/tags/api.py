from socket import error as SocketError

from flask import request, abort, jsonify, current_app

from app import db, mpd
from app.models import Tag
from app.schemas import tag_schema
from app.tags import bp


def mpd_command(command=None, args=None):
    try:
        mpd.connect(current_app.config["MPD_HOST"], current_app.config["MPD_PORT"])
    except:
        return 'could not establish connection to mpd'

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
    return response


@bp.route('/tags/api/<uid>', methods=['GET'])
def find_by_uid(uid):
    tag = Tag.query.filter_by(uid=uid).first()
    if tag is None:
        response = jsonify({'error': "'" + uid + "' not fond"})
        response.status_code = 404
        return response

    return tag_schema.jsonify(tag)


@bp.route('/tags/api/', methods=['POST'])
def store_uid():
    if not request.json or 'uid' not in request.json:
        response = jsonify({'error': "UID is mandatory"})
        response.status_code = 400
        return response

    tag = Tag(uid=request.json.get('uid'))
    db.session.add(tag)
    db.session.commit()
    return tag_schema.jsonify(tag)


@bp.route('/tags/api/status', methods=['GET'])
def status():
    mpd_status = mpd_command('status')
    return jsonify({'status': mpd_status})


@bp.route('/tags/api/currentsong', methods=['GET'])
def currentsong():
    mpd_status = mpd_command('currentsong')
    return jsonify({'status': mpd_status})


@bp.route('/tags/api/play/<uid>', methods=['GET'])
def play_by_uid(uid):
    tag = Tag.query.filter_by(uid=uid).first()

    if tag is None:
        response = jsonify({'error': "'" + uid + "' not fond"})
        response.status_code = 404
        return response

    if tag.path is None:
        response = jsonify({'status': "'" + uid + "' not assigned"})
        response.status_code = 404
        return response

    mpd_status = mpd_command('play', tag.path)
    return jsonify({'status': mpd_status})


@bp.route('/tags/api/pause', methods=['GET'])
def pause():
    mpd_status = mpd_command('pause')
    return jsonify({'status': mpd_status})


@bp.route('/tags/api/stop', methods=['GET'])
def stop():
    mpd_status = mpd_command('stop')
    return jsonify({'status': mpd_status})


@bp.route('/tags/api/next', methods=['GET'])
def next():
    mpd_status = mpd_command('next')
    return jsonify({'status': mpd_status})


@bp.route('/tags/api/prev', methods=['GET'])
def prev():
    mpd_status = mpd_command('prev')
    return jsonify({'status': mpd_status})

