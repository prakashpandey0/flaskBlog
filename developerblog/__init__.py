from flask import Flask

app  = Flask(__name__)

from developerblog.core.views import core
app.register_blueprint(core)

from developerblog.errors_page.handlers import errors_page
app.register_blueprint(errors_page)
