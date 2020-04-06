
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from jerrysblog.forms import CKTextAreaField
from flask_ckeditor import CKEditorField
from flask_login import login_required, current_user
from jerrysblog.extensions import admin_permission

class CustomView(BaseView):
    """查看自定义的flask-admin的功能"""

    # baseview的子类可以定义多个视图函数，使用@expose装饰器来注册函数为视图，这与一般的视图函数有区别的。

    @expose('/')
    @login_required
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    @login_required
    @admin_permission.require(http_exception=403)
    def second_page(self):
        return self.render('admin/second_page.html')

class CustomModelView(ModelView):
    """flask-admin的模型"""
    def is_accessible(self):
        column_display_pk=True
        return current_user.is_authenticated() and admin_permission.can()

class PostView(CustomModelView):
    """后台的新建和编辑"""

    #  form_overrides 指定使用新的字段类型 CKTextAreaField 替换原来的 TextAreaField
    form_overrides = dict(text=CKEditorField)

    # column_searchable_list 指定一个搜索框, 和搜索的范围为 post.text/post.title
    column_searchable_list = ('text','title')

    #  column_filters 指定一个过滤器, 筛选更加精确的值
    column_filters = ('publish_date',)

    # create_template/edit_template 指定自定义模板文件
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated() and admin_permission.can()
