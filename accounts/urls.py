from django.urls import path
from . import views

urlpatterns = [
    path('register/',       views.register_view,   name='register'),
    path('login/',          views.login_view,       name='login'),
    path('alt-login/',      views.alt_login_view,   name='alt_login'),
    path('logout/',         views.logout_view,      name='logout'),
    path('profile/',        views.profile_view,     name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('users/',          views.admin_users_view, name='admin_users'),
    path('users/create/',   views.create_user_view, name='create_user'),
    path('users/<int:user_id>/toggle/', views.toggle_user_view, name='toggle_user'),
]
