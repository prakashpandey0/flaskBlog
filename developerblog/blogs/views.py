from flask import render_template, url_for, Blueprint, flash, redirect,request
from flask_login import current_user, login_required

from developerblog import db
from developerblog.models import BlogPost
from developerblog.blogs.forms  import BlogPostForm


blogs = Blueprint('blogs',__name__)

#create
@blogs.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog = BlogPost(
                        text = form.text.data,
                        title = form.title.data,
                        user_id = current_user.id)
        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('core.index'))

    return render_template('blog_create.html', form = form)

#view
@blogs.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    print("view inside")
    blog = BlogPost.query.get_or_404(blog_post_id)

    return render_template('view_blog.html', title = blog.title, text = blog.text, id = blog.id,author=blog.author)

#update
@blogs.route('/<int:blog_post_id>/update',methods=["GET","POST"])
@login_required
def update(blog_post_id):
    blog = BlogPost.query.get_or_404(blog_post_id)
    if blog.author != current_user:
        abort(403)


    form = BlogPostForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.text  = form.text.data

        db.session.commit()
        return redirect(url_for('blogs.blog_post', blog_post_id = blog.id))
    elif request.method == "GET":
        form.title.data = blog.title
        form.text.data  = blog.text

    return render_template('blog_create.html', form = form)

#delete
@blogs.route('/<int:blog_post_id>/delete')
@login_required
def delete(blog_post_id):
    print("inside")
    blog = BlogPost.query.get_or_404(blog_post_id)

    if blog.author != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted Success!")
    return redirect(url_for('core.index'))
