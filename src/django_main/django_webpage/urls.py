from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # Method call name from views - name used on the HTML side
    # path("addfit", views.add_fit, name="addfit"),
    # path("addall", views.add_all, name="add"),
    # path("delete/<int:brain_id>", views.delete, name="delete"),
    # path("update/<int:todo_id>", views.update, name="update"),
]
