from django.urls import path
from . import views

urlpatterns = [
    path('superuser/home/', views.SuperUserHome.as_view(), name='superuser_home'),
    path('organizer/home/', views.AdminHome.as_view(), name='admin_home'),
    path('vendor/home/', views.VendorHome.as_view(), name='vendor_home'),
    path('register/', views.create_data, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]