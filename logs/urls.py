from django.urls import path
from . import views

urlpatterns = [
    path("", views.logs, name="logs"),
    path("new/", views.new_log, name="new_log"),

    path("<int:log_id>/", views.log, name="log"),
    path("<int:log_id>/new_entry/", views.new_entry, name="new_entry"),

    path(
        "edit_entry/<int:entry_id>/",
        views.edit_entry,
        name="edit_entry",
    ),
    
    path(
        "delete_entry/<int:entry_id>/",
        views.delete_entry,
        name="delete_entry",
    ),

    path(
        "edit_log/<int:log_id>/",
        views.edit_log,
        name="edit_log",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
]