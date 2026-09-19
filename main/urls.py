from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("project/", views.show_project, name="show_project"),
    path("project/add/", views.create_project, name="create_project"),
    path("project/<uuid:project_id>/delete/", views.delete_project, name="delete_project"),
    path("api/projects/", views.get_projects_json, name="get_projects_json"),
    path("experience/", views.show_experience, name="show_experience"),
    path("experience/add/", views.create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", views.edit_experience, name="edit_experience"),
    path("experience/<uuid:experience_id>/delete/", views.delete_experience, name="delete_experience"),
]
