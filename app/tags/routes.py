import os

from flask import render_template, flash, url_for, current_app
from werkzeug.utils import redirect, secure_filename

from app import db
from app.models import Tag
from app.tags import bp
from app.tags.forms import TagForm


@bp.route('/tags', methods=['GET'])
@bp.route('/tags/index', methods=['GET'])
def index():
    return render_template('tags/index.html', title='Tags', tags=Tag.query.order_by(Tag.id).all())


def get_music():
    result = []
    dir = os.listdir(current_app.config['MPD_MUSIC'])
    for entry in dir:
        result.append((entry, entry))
    return result


@bp.route('/tags/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    form = TagForm(obj=tag)
    form.path.choices = get_music()

    if form.validate_on_submit():
        if form.submit.data:
            tag.name = form.name.data
            tag.path = form.path.data
    
            artwork = form.artwork.data
            if artwork and allowed_file(artwork.filename):
                filename = secure_filename(artwork.filename)
                artwork.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                tag.artwork = filename
        
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('tags.index'))

    return render_template('tags/edit.html', title='Tags', form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/tags/<int:id>/delete', methods=['GET'])
def delete(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags.index'))
