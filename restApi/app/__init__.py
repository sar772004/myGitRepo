#for web form
from flask import Flask
#for flask config
from config import Config
#for db usage
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#for login management
from flask_login import LoginManager

#for email on error
import logging
from logging.handlers import SMTPHandler

#for logging to file
from logging.handlers import RotatingFileHandler
import os

#creates a flask app port
app = Flask(__name__)
#load the config.py class
app.config.from_object(Config)
#init the login manager for this app
login = LoginManager(app)

#for controlling what pages can be viewed
login.login_view = 'login'


#create a db instance
db = SQLAlchemy(app)
# create migration engine
migrate = Migrate(app, db)

#for importing the routes.py
from app import routes
#for importing models.py having the db structure
from app import models
#for importing errors.py to handle error pages
from app import errors

#logging when flask run is started with FLASK_DEBUG=0 only
if not app.debug:
    #logging to mail from mail server confgiured to ADMINS (which is to address), setup in config.py
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        print("mail handling")            
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    #for logging to file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')        

'''
adding a user to db:
u = User(username='srini', email='srini@ere.com')
u.set_password('cat')
db.session.add(u)
db.session.commit()
'''

