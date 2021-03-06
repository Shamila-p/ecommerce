from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('login', views.login, name='admin_login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='admin_logout'),
    path('user', views.user, name='admin_user'),
    path('user/add', views.add_user, name='add_user'),
    path('user/edit/<int:user_id>', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>', views.delete_user, name='delete_user'),
    path('user/block/<int:user_id>', views.block_user, name='block_user'),
    path('category', views.category, name='category'),
    path('category/add', views.add_category, name='add_category'),
    path('category/edit/<int:category_id>', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>', views.delete_category, name='delete_category'),
    path('product', views.product, name='product'),
    path('product/add', views.add_product, name='add_product'),
    path('product/edit/<int:product_id>', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('orders', views.orders, name='orders'),

    
]
