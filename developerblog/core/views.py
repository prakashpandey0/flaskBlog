from flask import render_template, request, Blueprint
from developerblog.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page  = request.args.get('page', 1, type=int)

    posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    print(posts)

    return render_template('index.html', posts = posts)


@core.route('/info')
def info():
    return render_template('info.html')
