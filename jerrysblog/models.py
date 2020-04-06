from flask_sqlalchemy import SQLAlchemy
from jerrysblog.extensions import bcrypt
from flask_login import AnonymousUserMixin
from uuid import uuid4
#from main import app

# INIT the sqlalchemy object                            
# Will be load the SQLALCHEMY_DATABASE_URL from config.py
# SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
db = SQLAlchemy()

users_roles = db.Table('users_roles',db.Column('user_id',db.String(45),db.ForeignKey('users.id')),db.Column('role_id',db.String(45),db.ForeignKey('roles.id')))

def create_uuid():
	return uuid4()

class User(db.Model):
	"""Represents Proected users."""

	# Set the name for table
	__tablename__ = 'users'
	id = db.Column(db.String(45), primary_key=True)
	username = db.Column(db.String(255))
	password = db.Column(db.String(255))
	# Establish contact with Post's ForeignKey: user_id
	posts = db.relationship('Post',backref='users',lazy='dynamic')

	roles = db.relationship('Role',secondary=users_roles,backref=db.backref('users',lazy='dynamic'))

	def __init__(self, id, username, password):
		self.id = id
		self.username = username
		self.password = self.set_password(password)

		default = Role.query.filter_by(name="default").one()
		self.roles.append(default)

	def __repr__(self):
		"""Define the string format for instance of User."""
		return "<Model User '{}'>".format(self.username)

	def set_password(self, password):
		"""加密密码,转换为哈希值"""
		return bcrypt.generate_password_hash(password)

	def check_password(self, password):
		"""检验输入的密码的哈希值与存储在数据库中的哈希值石佛一致"""
		return bcrypt.check_password_hash(self.password, password)

	def is_authenticated(self):
		"""检查用户是否登录"""

		if isinstance(self,AnonymousUserMixin):
			return False
		else:
			return True

	def is_active():
		"""检查用户是否通过验证"""

		return True

	def is_anonymous(self):
		"""检查是不是匿名登录"""

		if isinstance(self,AnonymousUserMixin):
			return True
		else:
			return False

	def get_id(self):
		"""返回User实例化对象的唯一标识id"""

		return str(self.id)


posts_tags = db.Table('posts_tags', db.Column('post_id', db.String(45), db.ForeignKey('posts.id')), db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))


class Post(db.Model):
	"""Represents Proected posts."""

	__tablename__ = 'posts'
	id = db.Column(db.String(45), primary_key=True,default=create_uuid)
	title = db.Column(db.String(45))
	text = db.Column(db.Text())
	publish_date = db.Column(db.DateTime)
	# set the foreign key for post
	user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
	comments = db.relationship('Comment',backref='posts',lazy='dynamic')
	tags = db.relationship('Tag',secondary=posts_tags,backref=db.backref('posts',lazy='dynamic'))

	def __init__(self, id,title):
		self.title = title
		self.id = id
#		self.text = text
#		self.publish_date = publish_date

	def __repr__(self):

		return "<Model Post `{}`".format(self.title)

class Comment(db.Model):
	"""Represents Proected comments."""

	__tablename__ = 'comments'
	id = db.Column(db.String(45),primary_key=True,default=create_uuid)
	name = db.Column(db.String(255))
	text = db.Column(db.Text())
	date = db.Column(db.DateTime())
	post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

	def __init__(self,id,name):
		self.name = name
		self.id = id

	def __rerp__(self):
		return "<Model Comment `{}`>".format(self.name)

class Tag(db.Model):
	"""Represents Proected tags."""

	__tablename__ = 'tags'
	id = db.Column(db.String(45), primary_key=True,default=create_uuid)
	name = db.Column(db.String(255))

	def __init__(self,id,name):
		self.name = name
		self.id = id

	def __repr__(self):
		return "<Model Tag `{}`>".format(self.name)

class Role(db.Model):

	__tablename__ = 'roles'

	id = db.Column(db.String(45),primary_key=True)
	name = db.Column(db.String(45),unique=True)
	description = db.Column(db.String(255))

	def __init__(self,id,name):
		self.id = id
		self.name = name

	def __repr__(self):
		return "<Model Role `{}`>".format(self.name)

class Reminder(db.Model):

	__tablename__ = 'reminders'

	id = db.Column(db.String(45),primary_key=True)
	date = db.Column(db.DateTime())
	email = db.Column(db.String(225))
	text = db.Column(db.Text())

	def __init__(self,id,text):
		self.id=id
		self.email = text

	def __repr__(self):
		return '<Model Reminder `{}`>'.format(self.text[:20])
