from django.urls import path

from database import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "add_brain_instance/<str:brain_instance>",
        views.add_brain_instance,
        name="add_brain_instance",
    ),
    path(
        "get_brain_instanceinstance/<int:brain_id>",
        views.get_brain_instance,
        name="get_brain_instanceinstance",
    ),
]
