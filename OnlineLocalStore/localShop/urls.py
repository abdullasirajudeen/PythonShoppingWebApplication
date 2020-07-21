from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index,name='index'),
    path('logout', views.logout,name='user_logout'),
    path('login', views.login,name='user_login'),
    path('signup', views.signup,name='user_signup'),
    path('search', views.search,name='product_search'),
    path('single', views.single,name='product_single'),
    path('checkout', views.checkout,name='checkout'),
    path('orderstatus', views.orderstatus,name='order_status'),
    path('viewcart', views.viewcart,name='cart_status'),
    path('addtocart', views.addtocart, name='cart_create'),
    path('removefromcart', views.removefromcart, name='removefromcart'),
    path('shopsnearme', views.shopsnearme, name='shopsnearme'),
    path('orderhistory', views.orderhistory, name='order_history'),
    path('shopproducts', views.shopproducts, name='shopproducts'),
    path('addreview', views.addreview,name='add_review'),
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),
    path('contact', views.contact,name='contact')
]