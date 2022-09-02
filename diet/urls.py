from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('intake/<str:calc_type>', views.intake, name='intake'),
    path('profile', views.profile, name='profile'),
    path('profile/search', views.profile, name='search'),

    # API route
    path('password', views.password, name='change_password'),
    path('intake/calc/<str:calc_type>', views.intake_calculator, name='calc'),
]