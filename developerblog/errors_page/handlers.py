from flask import render_template, Blueprint

errors_page  = Blueprint('errors_page',__name__)

@errors_page.app_errorhandler(404)
def error_404(error):
    #note: returning here tuple
    return render_template('errors_page/404.html'), 404

#for forbidden access
@errors_page.app_errorhandler(403)
def error_403(error):
    return render_template('errors_page/403.html'), 403
