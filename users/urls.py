from django.urls import path
from users.views import RegisterView, LoginView, HomeView, LogoutView, UserDetailView, SearchView

urlpatterns = [
    path("", SearchView.as_view()),
    path("home/", HomeView.as_view()),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("<slug:slug>/", UserDetailView.as_view()),
]
