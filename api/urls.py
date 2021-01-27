from django.urls import path, re_path

from . import adminviews
from . import targetviews
from . import articleviews
from . import keywordviews

app_name = 'api'   # 指定命名空间

urlpatterns = [
    path('article', articleviews.ArticleView.as_view(), name='新增post/获取所有get 文章'),
    path('articlefilter', articleviews.ArticleFilterView.as_view(), name='编辑put/条件查询post/删除delete 文章'),
    path('keyword', keywordviews.KeywordView.as_view(), name='编辑put/条件查询post/删除delete 关键字'),
    path('keywordfilter', keywordviews.KeywordFilterView.as_view(), name='编辑put/条件查询post/删除delete 关键字'),
    path('target', targetviews.TargetView.as_view(), name='编辑put/条件查询post/删除delete url'),
    path('targetfilter', targetviews.TargetFilterView.as_view(), name='编辑put/条件查询post/删除delete url'),
    path('admin/login', adminviews.LoginView.as_view(), name='login'),
    path('admin/info', adminviews.AdminInfoView.as_view(), name='info'),

]