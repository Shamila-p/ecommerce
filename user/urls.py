from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('user/profile', views.user_profile, name='user_profile'),
    path('user/edit', views.user_edit, name='user_edit'),
    path('user/changepassword', views.change_password, name='change_password'),
    path('product/view/<int:product_id>', views.view_more, name='view_more'),
    path('cart/add/<int:product_id>',views.cart_add,name="cart_add"),
    path('cart',views.cart,name="cart"),
    path('cart/remove/<int:cart_item_id>', views.remove_item, name='remove_item'),
    path('cart/quantity_add/<int:cart_item_id>', views.quantity_add, name='quantity_add'),
    path('cart/quantity_minus/<int:cart_item_id>', views.quantity_minus, name='quantity_minus'),
    path('cart/check_out',views.check_out,name='check_out'),
    path('order',views.order,name='order')



]
