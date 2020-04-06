from os import path

from flask import render_template, Blueprint,redirect,url_for
from sqlalchemy import func, extract
from flask_principal import Permission, UserNeed
#from main import app
from jerrysblog.models import db, User, Post, Tag, Comment, posts_tags

from uuid import uuid4
from datetime import datetime

from flask_login import login_required,current_user

from jerrysblog.forms import CommentForm,PostForm,SearchForm

import re
import requests
from bs4 import BeautifulSoup

blog_blueprint = Blueprint(
    'blog',
    __name__,
    # path.pardir ==> ..
    template_folder=path.join(path.pardir,'templates','blog'),
    url_prefix='/blog')

def sidebar():
    """目录"""

    totals = func.count(posts_tags.c.post_id).label('total')
    top_tags = db.session.query(
            Tag, totals).join(
            posts_tags
        ).group_by(Tag).order_by(totals.desc()).all()
    
    return top_tags


@blog_blueprint.route('/')

@blog_blueprint.route('/<int:page>', methods=('GET', 'POST'))
def home(page=1):
    """博客页面"""

    searchform = SearchForm()

    if searchform.validate_on_submit():
        posts = Post.query.filter(
            Post.title.like("%"+searchform.keyword.data+"%")
            ).order_by(
                Post.publish_date.desc()).paginate(page, 10)
    else:
        posts = Post.query.order_by(
            Post.publish_date.desc()
        ).paginate(page, 10)

    top_tags = sidebar()

    return render_template('home.html',
                            page=page,
                            posts=posts,
                            searchform=searchform,
                            top_tags=top_tags)

@blog_blueprint.route('/ctf/<int:page>', methods=('GET', 'POST'))
def ctf_blog(page=1):
    """ctf博客页面"""

    searchform = SearchForm()

    if form.validate_on_submit():
        posts = Post.query.join(posts_tags).filter(
            Post.title.like("%"+searchform.keyword.data+"%"),Tag.name=="ctf"
            ).order_by(
                Post.publish_date.desc()).paginate(page, 10)
    else:
        posts = db.session.query(Post).join(posts_tags).filter(
                                                    Tag.name == "ctf"
                                                    ).order_by(
                                                    Post.publish_date.desc()
                                                    ).paginate(page, 10)

    return render_template('ctf_blog.html',
                            posts=posts,
                            page=page,
                            searchform=searchform)

        


@blog_blueprint.route('/post/<string:post_id>', methods=('GET', 'POST'))
def post(post_id):
    """View function for post page"""

    # form object: 'Comment'
    searchform = SearchForm()
    commentform = CommentForm()
    # 在视图函数中创建一个 form 对象, 并以此来获取用户在输入框中输入的数据对象
    # form.validata_on_submit() 方法会隐式的判断该 HTTP 请求是不是 POST, 若是, 则将请求中提交的表单数据对象传入上述的 form 对象并进行数据检验.    # 若提交的表单数据对象通过了 form 对象的检验, 则 form.validata_on_submit() 返回为 True 并且将这些数据传给 form 对象, 成为其实例属性.
    if searcgform.validate_on_submit():
        posts = Post.query.join(posts_tags).filter(
            Post.title.like("%"+searchform.keyword.data+"%"),Tag.name=="ctf"
            ).order_by(
                Post.publish_date.desc()).paginate(page, 10)

    if commentform.validate_on_submit():
        new_comment = Comment(id=str(uuid4()),name=commentform.name.data)
        new_comment.text = commentform.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.now()
        db.session.add(new_comment)
        db.session.commit()

    post = db.session.query(Post).get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           searchform=searchform,
                           commentform=commentform)

@blog_blueprint.route('/new',methods=['GET','POST'])
@login_required
def new_post():
    """新建博客文章"""

    postform = PostForm()

    searchform = SearchForm()

    if not current_user:
        return redirect(url_for(main.login))

    if postform.validate_on_submit():
        new_post = Post(id=str(uuid4()),title=postform.title.data)
        new_post.text = postform.text.data
        new_post.publish_date = datetime.now()
        new_post.users = current_user

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.home'))

    return render_template('new_post.html',postform=postform,searchform=searchform)

@blog_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_post(id):
    """编辑博客"""

    post = Post.query.get_or_404(id)

    if not current_user:
        return redirect(url_for('main.login'))

    if current_user != post.users:
        return redirect(url_for('blog.post',post_id=id))

    permission = Permission(UserNeed(post.users.id))
    if permission.can() or admin_permission.can():
        postform = PostForm()

        if postform.validate_on_submit():
            data1 = str(postform.text).replace("required>","&")
            data2 = str(data1).replace("</textarea>"," ")
            mes = data2.find("&")
            data = data2[mes+1:]

            post.title = postform.title.data
            post.text = data
            post.publish_date = datetime.now()

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.post',post_id=post.id))
    else:
        abort(403)


    postform.title.data  = post.title
    postform.text.data = post.text
    return render_template('edit_post.html',postform=postform,post=post)

@blog_blueprint.route('/归档', methods=['GET', 'POST'])
def guidang():
    searchform = SearchForm()

    count = db.session.query(func.count(Post.id)).all()
    posts = db.session.query(extract('year',Post.publish_date),extract('month',Post.publish_date).label('month'),Post).group_by(Post.publish_date.desc()).order_by(Post.publish_date.desc()).all()
    length = len(posts)

    top_tags = sidebar()
    return render_template('归档.html',
                            count = count,
                            posts=posts,
                            length=length,
                            top_tags=top_tags,
                            searchform=searchform)

@blog_blueprint.route('/tag/<string:tag_name>')
@blog_blueprint.route('/tag/<string:tag_name>/<int:page>', methods=['GET', 'POST'])
def tag(tag_name,page=1):
    """View function for tag page"""
    searchform = SearchForm()

    posts = db.session.query(Post).join(posts_tags).filter(Tag.name=="CTF真题").order_by(Post.publish_date.desc()).paginate(page, 10)
    #tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
    # posts = tag.posts.order_by(Post.publish_date.desc()).all()

    top_tags = sidebar()

    return render_template('home.html',
                           tag=tag,
                           posts=posts,
                           searchform=searchform,
                           page=page,
                           top_tags=top_tags)


@blog_blueprint.route('/user/<string:username>', methods=['GET', 'POST'])
def user(username):
    """View function for user page"""

    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()

    return render_template('user.html',
                           user=user,
                           posts=posts)
