from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_page, name="new"),
    path("wiki/<str:title>", views.entry_page, name="entry"),
    path("search", views.search_page, name="search"),
    path("edit", views.edit_page, name="edit"),
    path("save", views.save_page, name="save"),
    path("update", views.update_page, name="update"),
    path("random", views.random_page, name="random"),
    
]
