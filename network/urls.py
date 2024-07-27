
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:uid>", views.view_profile, name="view_profile"),
    path("following", views.following_feed, name="following"),
    path("network", views.network, name="network"),

    # API Routes
    path("posts/<int:post_id>", views.post, name="post"),
    path("likes/<int:post_id>", views.likefn, name="likes"),
]
