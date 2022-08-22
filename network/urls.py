
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/following", views.following, name="following"),

    # API
    path("api/post/<int:post_id>", views.api_post, name="post"),
    path("api/profile/<int:profile_id>", views.api_profile,name="api_profile")
]
