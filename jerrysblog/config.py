class Config(object):
	"""Base config class."""
	# WTForm secret key
	SECRET_KEY = '041cadc03de2e9bde9fdcee99981e498'
	#  reCAPTCHA Public key and Private key
	RECAPCHA_PUBLIC_KEY = "6LcM5NgUAAAAADyjPZkPZoMA8yAbQNcnDKYVwgi0"
	RECAPTCHA_PRIVATE_KEY = "6LcM5NgUAAAAAFJiZfpslJYGn4-i-VF-2wD-rbr3"


class ProdCondig(Config):
	"""Production config class."""
	pass

class DevConfig(Config):
	"""Development config class."""
	#Open the DEBUG
	DEBUG = True
	# Mysql connetcion
	SQLALCHEMY_DATABASE_URI = 'mysql://root@127.0.0.1:3306/jerrysblog'
	#Celery<-->RabbitMQ connection
	CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
	CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"

	# 在开发环境中不进行打包
	ASSETS_DEBUG = True
