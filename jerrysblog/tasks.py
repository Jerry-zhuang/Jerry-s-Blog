import smtplib
import datetime
from email.mime.text import MIMEText

from flask_mail import Message

from jerrysblog.extensions import flask_celery,mail

@flask_celery.task(
    bind=True,
    igonre_result=True,
    default_restry_delay=300,
    max_retries=5)
def remind(self, primary_key):
    """注册时发送邮件"""

    reminder = Reminder.query.get(primary_key)

    msg = MIMEText(reminder.text)
    msg['Subject'] = 'Welcome!'
    msg['FROM'] = '3312326133@qq.com'
    msg['To'] = reminder.email

    try:
        smtp_server = smtplib.SMTP('localhost')
        smtp_server.starttls()
        smtp_server.login('3312326133@qq.com','959is959')
        smtp_server.sendmail('3312326133@qq.com',[reminder.email],msg.as_string())
        smtp_server.close()
        return

    except Exception as err:
        self.retry(exc=err)

def on_reminder_save(mapper,connect,self):
    """任务提醒"""

    remind.apply_async(args=(self.id), eta=self.date)
