from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('contact', views.contact, name="contact"),
    path('faq', views.faq, name="faq"),
    path('faq/<int:question_id>', views.question, name="question"),
    path('dates', views.dates, name="dates"),

    # API route
    path('faq/<int:question_id>/comment', views.comment, name="comment"),
    path('faq/<int:comment_id>/vote', views.vote, name="vote"),
]