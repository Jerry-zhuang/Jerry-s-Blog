from os import path
from uuid import uuid4

from flask import flash, url_for, redirect, render_template, Blueprint
from jerrysblog.forms import LoginForm, RegisterForm,OpenIDForm,SearchForm
from jerrysblog.extensions import openid
from jerrysblog.models import db, User,Role
from flask_login import login_user,logout_user
from flask_principal import identity_changed,current_app,Identity, AnonymousIdentity

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'main'))

@main_blueprint.route('/')
def index():
	return redirect(url_for('blog.home'))

@main_blueprint.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login():
	"""登录模块"""

	loginform = LoginForm()

	openid_form = OpenIDForm()

	searchform = SearchForm()

	if openid_form.validate_on_submit():
		return openid.trg_login(
			openid_form.openid_url.data,
			ask_for=['nickname', 'email'],
			ask_for_optional=['fullname'])
	openid_errors = openid.fetch_error()
	if openid_errors:
		flash(openid_errors, category="danger")

	if loginform.validate_on_submit():

		user = User.query.filter_by(username=loginform.username.data).one()
		# 将已登录并通过load_user()的用户对应的User对象，保存在session中，所以该用户可以在访问不同页面时不需要重复登录
		login_user(user,remember=loginform.remember.data)

		identity_changed.send(current_app._get_current_object(),identity=Identity(user.id))

		"""flash("登录成功",category="success")"""
		return redirect(url_for('blog.home'))

	return render_template('login.html',loginform=loginform,openid_form=openid_form,searchform=searchform)

@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
	"""退出登录模块"""

	# 使用logout_user来将用户从session中删除
	logout_user()

	identity_change.send(current_app._get_current_object(),identity=AnonymousIdentity())

	flash("退出登录",category="success")
	return redirect(url_for('main.login'))

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
	"""注册模块"""

	searchform=SearchForm()

	registerform = RegisterForm()

	if registerform.validate_on_submit():
		new_user = User(id=str(uuid4()),username=registerform.username.data,password=form.password.data)

		db.session.add(new_user)
		db.session.commit()

		flash('注册成功，请登录',category="success")

		return redirect(url_for('main.login'))
	return render_template('register.html',registerform=registerform,searchform=searchform)
