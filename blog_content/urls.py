from django.urls import path
from blog_content.views import PostCategory, PostDetail, PostIndex, PostSearch

app_name = 'blog_content'

urlpatterns = [
    path('', PostIndex.as_view(), name='index'),
    path('details/<int:pk>/<str:slug>/', PostDetail.as_view(), name='details'),
    path('category/<str:slug>/', PostCategory.as_view(), name='category'),
    path('search/', PostSearch.as_view(), name='search'),
]
