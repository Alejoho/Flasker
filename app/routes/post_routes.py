from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import PostForm
from app.models import Post
from app import db

bp = Blueprint("post_routes", __name__)


@bp.route("/add-post", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            author=form.author.data,
            slug=form.slug.data,
            content=form.content.data,
        )

        form.title.data = ""
        form.author.data = ""
        form.slug.data = ""
        form.content.data = ""

        # TODO: look up how to migrate the last changes to the db using the new structure of the app
        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submited Successfuly")

        return redirect(url_for("post_routes.posts"))

    return render_template("add_post.html", form=form)


@bp.route("/posts")
def posts():
    posts = Post.query.order_by(Post.date_posted).all()
    # posts = db.session.query(Post).order_by(Post.date_posted).all()

    return render_template("posts.html", posts=posts)


@bp.route("/posts/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)

    return render_template("post.html", post=post)
