from django.urls import path

from .views import posts_list, post_create, post_edit, post_delete, home

urlpatterns = [
    path('', home, name='home'),
    path('posts-list', posts_list, name='posts_list'),
    path('create', post_create, name='post_create'),
    path('edit/<int:id>', post_edit, name='post_edit'),
    path('delete/<int:id>', post_delete, name='post_delete'),
]