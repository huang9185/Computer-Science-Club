from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:item>", views.category, name="category"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("listing/<int:listing_id>/feed", views.feed, name="feed"),
    path("listing/<int:listing_id>/edit_watch", views.edit_watch, name="edit_watch"),
    path("listing/<int:listing_id>", views.listings, name="listing")
]
