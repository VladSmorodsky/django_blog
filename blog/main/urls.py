from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<str:slug>/', views.post_detail, name='post_detail'),
    path('posts/<str:slug>/comments/add', views.add_comment_view, name='add_comment'),
    path('tags/<str:tag_slug>', views.post_list, name='post_tag_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
