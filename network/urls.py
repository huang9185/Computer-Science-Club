
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # API routes
    path("posts", views.compose, name="compose"),
    path("posts/all", views.postbox, name="postbox"),
    path("follow/<int:poster_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("posts/<int:user_id>", views.postbox, name="postbox"),
    path("users/<int:poster_id>", views.profile, name="profile")
]
