from app import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(), unique=True)
    name = db.Column(db.String(), nullable=True)
    path = db.Column(db.String(), nullable=True)
    artwork = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.uid)

