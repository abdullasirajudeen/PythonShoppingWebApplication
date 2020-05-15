from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('login', views.login,name='store_login'),
    path('signup', views.signup,name='store_signup'),
    path('index', views.index,name='store_index'),
    path('logout', views.logout,name='store_logout'),
    path('addproduct', views.addproduct,name='store_addproduct'),
    path('single', views.single,name='store_single'),
    path('neworders', views.neworders,name='new_orders'),

]