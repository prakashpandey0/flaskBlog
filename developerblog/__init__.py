from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app  = Flask(__name__)

app.config['SECRET_KEY'] = "prakash"

######################################
##########  DATABASE #################
######################################

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@localhost/flaskblog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#connecting application to the database
Migrate(app,db)



#########################################
#### Login config

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'



#########################################




from developerblog.core.views import core
app.register_blueprint(core)

from developerblog.errors_page.handlers import errors_page
app.register_blueprint(errors_page)


from developerblog.users.views import users
app.register_blueprint(users)

from developerblog.blogs.views import blogs
app.register_blueprint(blogs)
