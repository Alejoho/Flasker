from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import select
from app.forms import PostForm, SearchForm
from app.models import Post
from app import db

bp = Blueprint("post_routes", __name__)


@bp.route("/add-post", methods=["GET", "POST"])
# @login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            # author=form.author.data,
            slug=form.slug.data,
            content=form.content.data,
            user_id=current_user.id,
        )

        form.title.data = ""
        # form.author.data = ""
        form.slug.data = ""
        form.content.data = ""

        db.session.add(post)
        db.session.commit()

        flash("Post Has Been Created")

        return redirect(url_for("post_routes.posts"))

    return render_template("post/add_edit_post.html", form=form, post=None)


@bp.route("/posts")
def posts():
    posts = Post.query.order_by(Post.date_posted).all()
    # posts = db.session.query(Post).order_by(Post.date_posted).all()

    return render_template("post/posts.html", posts=posts)


@bp.route("/posts/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)

    return render_template("post/post.html", post=post)


@bp.route("/posts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    if check_owner(post.user_id) == False:
        flash("You can't edit a post you don't own!!")
        return redirect(url_for("post_routes.posts"))

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        try:
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            flash("There was an error editing the post")

        flash("Post Has Been Updated!")

        return redirect(url_for("post_routes.posts"))

    form.title.data = post.title
    # form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content

    return render_template("post/add_edit_post.html", form=form, post=post)


@bp.route("/posts/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    if check_owner(post.user_id) == False:
        flash("You can't delete a post you don't own!!")
        return redirect(url_for("post_routes.posts"))

    db.session.delete(post)
    try:
        db.session.commit()
    except Exception as err:
        print(err)
        flash("There was an error deleting the post")

    flash("Post Has Been Deleted")

    return redirect(url_for("post_routes.posts"))


def check_owner(user_id):
    return user_id == current_user.id


@bp.post("/search")
def search():
    form = SearchForm()

    if form.validate_on_submit():
        term_searched = form.searched.data

        stmt = select(Post)
        stmt = stmt.where(Post.content.like("%" + term_searched + "%"))
        stmt = stmt.order_by(Post.title)
        print(stmt)
        posts = list(db.session.scalars(stmt))
        # posts = db.session.execute(stmt)
        return render_template(
            "post/search.html", term_searched=term_searched, posts=posts
        )


@bp.app_context_processor
def base_context():
    form = SearchForm()
    return dict(form=form)
    # return dict(form=form, test="ale")
