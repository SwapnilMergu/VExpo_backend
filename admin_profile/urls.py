from django.urls import path
from . import views

urlpatterns = [
    path('superuser/organizer/', views.admin_list, name='view_admin'),
    path('superuser/organizer/create', views.create_admin, name='create_admin'),
    path('superuser/organizer/update/<int:pk>', views.update_admin, name='update_admin'),
    path('superuser/organizer/delete/<int:pk>', views.delete_admin, name='delete_admin'),
    path('organizer/profile',views.organizer_profile,name="organizer_profile"),
    path('organizer/profile/update',views.update_admin_profile,name="update_admin_profile")
]