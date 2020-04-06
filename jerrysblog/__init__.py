import os

from flask import Flask,redirect,url_for
from .config import DevConfig
from sqlalchemy import event
from .models import Reminder,Role,Tag,db,Post
from .controllers import blog,main,admin
from .extensions import bcrypt,pagedown,openid,login_manager,principals,flask_celery,flask_admin,ckeditor
from .extensions import assets_env,main_js,main_css
from .tasks import on_reminder_save

from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user

def create_app(object_name):


	app = Flask(__name__)

	# 所有视图函数都搬离app，但app不能没有试图函数，所以定义一个根目录视图函数，本且重定向到蓝图blog的home（）中

#	@app.route('/')
#	def index():
#		return redirect(url_for('blog.home'))

# 1. Get the config from object of DecConfig
#    使用 config.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载 class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。

# 2. set the app config

	app.config.from_object(object_name)

	db.init_app(app)
	# 初始化项目
	bcrypt.init_app(app)

	openid.init_app(app)

	pagedown.init_app(app)

	login_manager.init_app(app)

	principals.init_app(app)

	flask_celery.init_app(app)

	event.listen(Reminder, 'after_insert', on_reminder_save)

	ckeditor.init_app(app)

	#### 初始化flask-assets项目
	assets_env.init_app(app)
	assets_env.register('main_js', main_js)
	assets_env.register('main_css', main_css)

	#### flask_admin
	flask_admin.init_app(app)
	# CustomView
	flask_admin.add_view(admin.CustomView(name='游客'))
	# 
	models = [Role,Tag,Reminder]
	for model in models:
		flask_admin.add_view(admin.CustomModelView(model,db.session,category='常用模块'))
	flask_admin.add_view(admin.PostView(Post, db.session, category='文章管理'))
	flask_admin.add_view(admin.CustomFileAdmin(os.path.join(os.path.dirname(__file__),'static'),'/static',name='Static Files'))


	@identity_loaded.connect_via(app)
	def on_identity_loaded(sender,identity):

		identity.user = current_user

		if hasattr(current_user,'id'):
			identity.provides.add(UserNeed(current_user.id))
		if hasattr(current_user, 'roles'):
			for role in current_user.roles:
				identity.provides.add(RoleNeed(role.name))
# 指定 URL='/' 的路由规则
# 当访问 HTTP://server_ip/ GET(Default) 时，call home()
#@app.route('/')
#def home():
#	return '<h1>Hello World!</h1>'

# 将新建的蓝图对象注册到app中
	app.register_blueprint(blog.blog_blueprint)
	# 这样的话, app 对象就拥有了两个蓝图, 其中 blog 提供博客内容的管理和展示功能, main 提供了网站的账户管理功能. 
	#  因为在 URL /下包含了博客首页和用户登录两个视图, 所以在两个蓝图中都必须含有对 / 进行处理的视图函数

	app.register_blueprint(main.main_blueprint)

	return app

if __name__ == '__main__':
	app.run()
