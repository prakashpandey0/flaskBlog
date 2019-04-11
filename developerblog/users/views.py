from flask import render_template, request , Blueprint, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required

from developerblog import db
from developerblog.models import User, BlogPost
from developerblog.users.forms import LoginForm, RegistrationForm,UpdateUserForm
from developerblog.users.profile_handler import add_profile_pic

users = Blueprint('users',__name__)


@users.route('/register', methods=['GET','POST'])
def register():
    #creating an instance
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registration!")
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in success!')

            next = request.args.get('next')

            if(next == None or not next[0]=='/'):
                next  = url_for('core.index')

            return redirect(next)

    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.profile.data:
            username = current_user.username
            pic      = add_profile_pic(form.profile.data, username)
            current_user.profile = pic

        current_user.username  = form.username.data
        current_user.email     = form.email.data
        print(current_user.profile)
        db.session.commit()
        flash('Updated Success!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data  = current_user.username
        form.email.data    = current_user.email

    profile = url_for('static',filename='profile_pics/'+current_user.profile)
    return render_template('account.html', form = form, profile = profile)


@users.route('/<username>')
def posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    blog = BlogPost.query.filter_by(author = user).first().order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('blog_post.html', blog= blog, user = user)
