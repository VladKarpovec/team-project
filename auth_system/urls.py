from django.urls import path
from auth_system import views

app_name = "register"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("", views.home_auth, name="home_auth"),
    path("logout/", views.logout_view, name="logout"),
]
