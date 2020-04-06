# 该文件用来管理所有会使用到的Flask扩展

from flask_bcrypt import Bcrypt
from flask_pagedown import PageDown
from flask_login import LoginManager
from flask_openid import OpenID
from flask_principal import Principal, Permission, RoleNeed
from flask_celery import Celery
from flask_mail import Mail
from flask_assets import Environment, Bundle
from flask_admin import Admin
from flask_ckeditor import CKEditor

# 创建bcrypt实例
bcrypt = Bcrypt()

# 创建pagedown实例
pagedown = PageDown()

# 创建flask-celery-helper
flask_celery = Celery()

openid = OpenID()

# 创建flask-login的实例
login_manager = LoginManager()

# 创建Flask-Mail的实例
mail = Mail()

# 创建flask-assets的实例
assets_env = Environment()

main_css = Bundle(
    'css/bootstrap.css',
    'css/bootstrap-theme.css',
    filters='cssmin',
    output='assets/css/common.css')

main_js = Bundle(
    'js/bootstrap.js',
    filters='jsmin',
    output='assets/js/common.js')

# 创建flask-admin的实例
flask_admin = Admin()

# 设置login的参数

# 设置登录的视图函数
login_manager.login_view = "main.login"
# 一旦cookie被盗，重新登录
login_manager.session_protection = "strong"
#指定提供登录的文案
login_manager.login_message = "Pless login to access this page."
#指定登录信息的类别为info
login_manager.login_message_category = "info"

ckeditor = CKEditor()

@login_manager.user_loader
def load_user(user_id):
    """在用户登录并调用login_user时，根据user_id找到对应的user，如果没找到，返回none，此时的user_id将会自动从session中移除，如能找到user，则user_id会被继续保存"""

    from .models import User
    return User.query.filter_by(id=user_id).first()

# 创建principal实例
principals = Principal()
# 设置3种权限
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

