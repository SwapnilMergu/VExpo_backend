from django.urls import path
from . import views

urlpatterns = [
    path('organizer/vendor/', views.view_vendor, name='view_vendor'),
    path('organizer/vendor/create', views.create_vendor, name='create_vendor'),
    path('organizer/vendor/update/<int:pk>', views.update_vendor, name='update_vendor'),
    path('organizer/vendor/delete/<int:pk>', views.delete_vendor, name='delete_vendor'),
    path('vendor/home/users_visited/', views.users_visited, name='users_visited'),
    path('vendor/home/users_bookings/', views.users_bookings, name='users_bookings'),
    path('vendor/home/users_bookings/accept/<int:pk>', views.accept_booking, name='accept_user_booking'),
    path('vendor/home/users_bookings/reject/<int:pk>', views.reject_booking, name='reject_user_booking'),
    path("vendor/profile",views.view_profile,name="view_profile"),
    path("vendor/profile/edit",views.edit_profile,name="edit_profile")
    
]