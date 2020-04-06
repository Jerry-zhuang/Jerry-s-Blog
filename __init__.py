from flask import Flask,redirect,url_for
from jerrysblog.config import DevConfig
from jerrysblog.models import db

from jerrysblog.controllers import blog

app = Flask(__name__)

# 所有视图函数都搬离app，但app不能没有试图函数，所以定义一个根目录视图函数，本且重定向到蓝图blog的home（）中

@app.route('/')
def index():
	return redirect(url_for('blog.home'))

# Get the config from object of DecConfig
# 使用 config.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载 class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
app.config.from_object(DevConfig)

db.init_app(app)

# 指定 URL='/' 的路由规则
# 当访问 HTTP://server_ip/ GET(Default) 时，call home()
#@app.route('/')
#def home():
#	return '<h1>Hello World!</h1>'

# 将新建的蓝图对象注册到app中
app.register_blueprint(blog.blog_blueprint)

if __name__ == '__main__':
	app.run()
