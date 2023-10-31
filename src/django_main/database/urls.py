from django.urls import path

from database import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "save_brain_instance",
        views.save_brain_instance,
        name="save_brain_instance",
    ),
    # path(
    #     "get_brain_instanceinstance/<int:brain_id>",
    #     views.get_brain_instance,
    #     name="get_brain_instanceinstance",
    # ),
]
