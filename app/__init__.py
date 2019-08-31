import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from mpd import MPDClient

from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
ma = Marshmallow()
mpd = MPDClient()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    ma.init_app(app)

    mpd.timeout = 10
    mpd.idletimeout = None

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.tags import bp as tags_bp
    app.register_blueprint(tags_bp)

    if not app.debug and not app.testing:
        app.logger.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        app.logger.info('Kidsbox startup')

    return app


from app import models