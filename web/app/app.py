import os
from flask import Flask, render_template, send_file, abort, send_from_directory, request
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
application = app
client = app.test_client()
app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager
from calls import bp as calls_bp
from meds import bp as meds_bp
app.register_blueprint(auth_bp)
app.register_blueprint(calls_bp)
app.register_blueprint(meds_bp)

init_login_manager(app)

from models import Medic, Med, Checkup, Customer

@app.route('/')
def index():
    return render_template('index.html')

