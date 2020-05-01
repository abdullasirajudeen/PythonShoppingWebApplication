from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('login', views.login,name='store_login'),
    path('signup', views.signup,name='store_signup'),
    path('index', views.index,name='store_index'),
    path('logout', views.logout,name='store_logout'),
]