from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("getRandom", views.getRandom, name="getRandom"),
    path("<str:title>", views.entry, name="entry")
]
