from django.contrib import admin
from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostList.as_view()),
    path('news/', PostList.as_view(), name="post_list"),
    path('news/search/', PostSearch.as_view(), name="post_search"),
    path('news/<int:id>', PostDetail.as_view(), name="post_detail"),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]