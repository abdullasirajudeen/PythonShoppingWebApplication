from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index,name='index'),
    path('logout', views.logout,name='user_logout'),
    path('login', views.login,name='user_login'),
    path('search', views.search,name='product_search'),
    path('slogin', views.slogin,name='store_login'),
    path('ssignup', views.ssignup,name='store_signup'),
    path('storeindex', views.storeindex,name='store_index'),
]