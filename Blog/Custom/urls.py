from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('create/', create, name='create'),
    path('detail_post/<int:pk>', detail_post, name='detail_post'),
    path('sample_post', sample_post, name='sample_post'),
    path('user_posts/<int:pk>', user_post , name='user_post'),
    path('delete/<int:pk>', deletePost, name='delete'),
    path('update/<int:pk>', updatePost, name='update'),

    path('login/', userLogin, name='userLogin'),
    path('logout/', userLogout, name='userLogout'),
    path('register/', userRegister, name='userRegister'),
]