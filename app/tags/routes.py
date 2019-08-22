from flask import render_template, flash, url_for
from werkzeug.utils import redirect

from app import db
from app.models import Tag
from app.tags import bp
from app.tags.forms import TagForm


@bp.route('/tags', methods=['GET'])
@bp.route('/tags/index', methods=['GET'])
def index():
    return render_template('tags/index.html', title='Tags', tags=Tag.query.order_by(Tag.id).all())


@bp.route('/tags/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    form = TagForm(obj=tag)
    form.path.choices = [('Schwiizergoofe 6', 'Schwiizergoofe 6'), ('Schwiizergoofe 3', 'Schwiizergoofe 3')]

    if form.validate_on_submit():
        if form.submit.data:
            tag.name = form.name.data
            tag.path = form.path.data
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('tags.index'))

    return render_template('tags/edit.html', title='Tags', form=form)
