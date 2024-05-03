from django.urls import path
from . import views

urlpatterns = [
    path('organizer/categories',views.view_admin_categories,name="view_categories"),
    path('organizer/categories/create',views.add_categories,name="create_categories"),
    path('organizer/categories/update/<int:pk>',views.update_categories,name="update_categories"),
    path('organizer/categories/delete/<int:pk>',views.delete_categories,name="delete_categories"), 


    path('superuser/categories',views.view_super_categories,name="superuser_view_categories"),
    path('superuser/categories/create',views.superuser_add_categories,name="superuser_create_categories"),
    path('superuser/categories/update/<int:pk>',views.superuser_update_categories,name="superuser_update_categories"),
    path('superuser/categories/delete/<int:pk>',views.superuser_delete_categories,name="superuser_delete_categories"), 

]
