import os
# import flask script object
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from jerrysblog import create_app
from jerrysblog import models
from jerrysblog import config

#import jerrysblog.__init__
#import jerrysblog.models

# 从系统中获得环境名
env = os.environ.get('BLOG_ENV','dev')

# 通过工厂方法创建app
app = create_app('jerrysblog.config.%sConfig' % env.capitalize())
#app = create_app(config.__name__ + '.Config')
# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create some new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server(host='127.0.0.1', port=5000))
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
	"""Create a python CLI.

	return: Default import object
	type: `Dict`
	"""
	# 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
	return dict(app=app,db=models.db,User=models.User,Post=models.Post,Comment=models.Comment,Tag = models.Tag,Role = models.Role)

if __name__ == '__main__':
	manager.run()
