from django.urls import path

from database import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_instance/", views.add_all, name="add_instance"),
]
