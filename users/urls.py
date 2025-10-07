from django.urls import path
from users.views import (
    RegisterView,
    LoginView,
    HomeView,
    LogoutView,
    GoogleLoginView,
    UserDetailView,
    SearchView,
    RequestPasswordReset,
    ResetPassword,
    UsersViewSet
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("google/login/", GoogleLoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("request-password-reset/", RequestPasswordReset.as_view()),
    path("password-reset/", ResetPassword.as_view()),
    path("home/", HomeView.as_view()),
    path("all/", UsersViewSet.as_view()),
    path("", SearchView.as_view()),
    path("<slug:slug>/", UserDetailView.as_view()),
]
