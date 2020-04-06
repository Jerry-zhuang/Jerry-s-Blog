import os

from celery import Celery

from jerrysblog import create_app

def make_celery(app):
    """创建celery进程"""

    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):

        abstract = True

        def __call__(self,*args,**kwargs):
            """创建实例对象时执行"""

            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)

    celery.Task = ContextTask
    return celery

env = os.environ.get('BLOG_ENV','dev')
flask_app= create_app('jerrysblog.config.%sConfig' %env.capitalize())

celery = make_celery(flask_app)
