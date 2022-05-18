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

]
