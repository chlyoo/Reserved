from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment

from instance.config import config

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('Reserved')

from gridfs import GridFS
from gridfs.errors import NoFile

fs = GridFS(db)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True) # modified 20191108
	app.config.from_object(config[config_name])
	app.config.from_pyfile('config.py') 
	
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

    # attach routs and custom error pages here
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix="/auth")
	from .reserve import reserve as reserve_blueprint
	app.register_blueprint(reserve_blueprint,url_prefix="/reserve")
	from .manage import manage as manage_blueprint
	app.register_blueprint(manage_blueprint, url_prefix="/manage")
	from .mypage import mypage as mypage_blueprint
	app.register_blueprint(manage_blueprint, url_prefix="/mypage")
	
	return app
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment

from instance.config import config

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('Reserved')

from gridfs import GridFS
from gridfs.errors import NoFile

fs = GridFS(db)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True) # modified 20191108
	app.config.from_object(config[config_name])
	app.config.from_pyfile('config.py') 
	
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

    # attach routs and custom error pages here
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix="/auth")
	from .reserve import reserve as reserve_blueprint
	app.register_blueprint(reserve_blueprint,url_prefix="/reserve")
	from .manage import manage as manage_blueprint
	app.register_blueprint(manage_blueprint, url_prefix="/manage")
	from .mypage import mypage as mypage_blueprint
	app.register_blueprint(manage_blueprint, url_prefix="/mypage")
	
	return app
