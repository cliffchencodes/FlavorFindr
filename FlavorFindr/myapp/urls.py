from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("query/", views.query, name="query"),
    path("results/", views.results, name="results"),
    path("success/", views.success, name="success"),
    path("add-item/", views.add_item, name="add_item"),
    path("groupby/", views.group_by, name="group_by"),
    path("edit-item/", views.edit_item, name="edit_item"),
    path(
        "edit-item/<str:name>/", views.edit_item, name="edit_item"
    ),  # Make sure to capture the 'name' parameter
    path("call-flask-api/", views.call_flask_api, name="call_flask_api"),
    path("add-food-to-flask/", views.add_food_to_flask, name="add_food_to_flask"),
]
