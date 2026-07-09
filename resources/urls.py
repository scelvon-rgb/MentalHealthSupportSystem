from django.urls import path
from . import views

urlpatterns = [

    # View all resources
    path(
        "",
        views.resource_list,
        name="resource_list"
    ),

    # Add a new resource
    path(
        "add/",
        views.add_resource,
        name="add_resource"
    ),

    # View one resource
    path(
        "<int:resource_id>/",
        views.resource_detail,
        name="resource_detail"
    ),

    # Edit a resource
    path(
        "edit/<int:resource_id>/",
        views.edit_resource,
        name="edit_resource"
    ),

    # Delete a resource
    path(
        "delete/<int:resource_id>/",
        views.delete_resource,
        name="delete_resource"
    ),

]