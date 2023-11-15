from django.urls import path

from vpn_service import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('create_site/', views.create_site, name='create_site'),
    path('<str:user_site_name>/<path:routes_on_original_site>', views.proxy_view, name='proxy'),
]
