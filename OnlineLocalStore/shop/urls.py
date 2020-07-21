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
    path('orderhistory', views.orderhistory,name='order_history'),
    path('viewproducts', views.viewproducts,name='view_products'),
    path('ordercompleted', views.ordercompleted,name='order_completed'),
	path('editproduct', views.editproduct,name='edit_product'),
	path('marksold', views.marksold,name='mark_soldout'),
	path('deleteproduct', views.deleteproduct,name='delete_product'),
    path('contact', views.contact,name='contact'),
]