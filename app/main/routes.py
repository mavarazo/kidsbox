import operator
import os

from flask import abort, current_app, render_template, send_from_directory
from werkzeug.security import safe_join

from app.main import bp
from app.main.album import Album
from app.main.track import Track
from app.models import Tag


@bp.route('/', methods=['GET'], defaults={'albumname': None})
@bp.route('/<albumname>', methods=['GET'])
def index(albumname):
    albums = get_music()
    selected_album = None
    if albumname:
        current_app.logger.info(f"Looking for {albumname}")
        for album in albums:
            if albumname == album.name:
                selected_album = album
                current_app.logger.info(f"Selected Album: {selected_album}")

    return render_template('main/index.html', title='Home', albums=albums, selected_album=selected_album)


def get_music():
    result = []
    for path in os.listdir("/app/music"):
        album = Album(name=path, artwork=get_artwork(path), tracks=get_tracks(path))
        current_app.logger.info(f"Found {album}")
        result.append(album)
    
    return sorted(result, key=operator.attrgetter("name"))


def get_artwork(path):
    for file in os.listdir(os.path.join("/app/music", path)):
        if file.endswith((".jpg", ".png", "jpeg")):
            return file


def get_tracks(path):
    result = []
    for file in os.listdir(os.path.join("/app/music", path)):
        if file.startswith("."):
            continue
        if file.endswith(".mp3"):
            result.append(Track(name=file))
    
    return sorted(result, key=operator.attrgetter("name"))


@bp.route('/music/<albumname>/<filename>')
def get_file_from_music_folder(albumname, filename):
    path = safe_join(os.path.join("/app/music", albumname))
    if path is None:
        abort(404, description=f"Resource \”{path}\” not found")
    return send_from_directory(path, filename)


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
