from django.urls import path
from . import views

urlpatterns = [
    path("vendor/stall/",views.view_stall,name="add_stall"),
    path("vendor/stall/create",views.create_stall,name="create_stall"),
]
