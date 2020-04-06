from flask_wtf import FlaskForm,RecaptchaField
from wtforms import widgets,StringField, TextField,TextAreaField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired, Length,EqualTo,URL
from flask_pagedown.fields import PageDownField

from jerrysblog.models import User

class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('用户名',[DataRequired(),Length(max=255)])
    password = PasswordField('密码',[DataRequired()])
    remember = BooleanField("记住密码")
 
#LoginForm 重载的 validate() 中调用了父类 Form 中的 validate()，用于检验用户输入的数据是否通过了 username/password 字段的检验器。

#LoginForm 重载的 validate() 不仅仅实现了父类的功能，还实现了检验 username 是否存在和用户输入的 password 是否正确的功能。子类重载父类的方法结合 super() 内置函数是 Python OOP 中常用的技巧。

    def validate(self):
        """验证账户信息"""

        check_validata = super(LoginForm,self).validate()

        if not check_validata:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.uername.errors.append('无效的用户名或密码')
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append('无效的用户名或密码')
            return False

        return True

class RegisterForm(FlaskForm):
    """register form"""

    username = StringField('用户名',[DataRequired(),Length(max=255)])
    password = PasswordField('密码', [DataRequired(), Length(min=8)])
    comfirm = PasswordField('确认密码', [DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('用户名已存在')
            return False

        return True

class PostForm(FlaskForm):
    """新建和编辑表单"""

    title = StringField('标题',[DataRequired(),Length(max=255)])
    text = TextAreaField('内容',[DataRequired()])

class CommentForm(FlaskForm):
    """Form vaildator for comment."""

    # 设置表单
    name = StringField(
        '姓名',
        validators=[DataRequired(), Length(max=255)])

    text = TextField(u'评论', validators=[DataRequired()])

class OpenIDForm(FlaskForm):
    """OpenID Form."""

    openid_url = StringField('OpenID URL', [DataRequired(), URL()])


class CKTextAreaWidget(widgets.TextArea):

    def __call__(self,field,**kwargs):
        kwargs.setdefault('class_','ckeditor')
        return super(CKTextAreaWidget,self).__call__(field,**kwargs)

class CKTextAreaField(TextAreaField):

    # 为该字段的HTML标签增加一个class
    widget = CKTextAreaWidget()

class SearchForm(FlaskForm):
    # 搜索框的表单

    keyword = StringField('关键词',[DataRequired(),Length(max=255)])