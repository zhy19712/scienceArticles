from django.urls import path

from api.views import targetview, keywordview, articleview, categoryview, centerview, adminview, systemview

app_name = 'api'   # 指定命名空间

urlpatterns = [
    path('article', articleview.ArticleView.as_view(), name='新增post/获取所有get 文章'),
    path('articlefilter', articleview.ArticleFilterView.as_view(), name='编辑put/条件查询post/删除delete 文章'),
    path('keyword', keywordview.KeywordView.as_view(), name='新增post/查询get 关键字'),
    path('keywordfilter', keywordview.KeywordFilterView.as_view(), name='编辑put/条件查询post/删除delete 关键字'),
    path('target', targetview.TargetView.as_view(), name='新增post/查询get 目标'),
    path('targetfilter', targetview.TargetFilterView.as_view(), name='编辑put/条件查询post/删除delete 目标'),
    path('category', categoryview.CategoryView.as_view(), name='新增post/查询get 分类'),
    path('categoryfilter', categoryview.CategoryFilterView.as_view(), name='编辑put/条件查询post/删除delete 分类'),
    path('admin/login', adminview.LoginView.as_view(), name='login'),
    path('admin/info', adminview.AdminInfoView.as_view(), name='info'),
    path('admin/user', adminview.UserView.as_view(), name='user增删改'),
    path('admin/userfilter', adminview.UserFilterView.as_view(), name='user查'),
    path('admin/userstatus', adminview.UserStatusView.as_view(), name='user status'),
    path('keywordtree', keywordview.KeywordTreeView.as_view(), name='post 构建关键字树'),
    path('center', centerview.CenterView.as_view(), name='get 获取中心'),
    path('globalsearch',articleview.GlobalSearchView.as_view(), name='post 全局搜索'),
    path('startcrawler',systemview.StartWeinxinView.as_view(), name='start weixin')
]