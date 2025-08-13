from django.urls import path
from users.views import Register, UserLoginView, Home, LogoutView

urlpatterns = [
    path("home/", Home.as_view()),
    path("register/", Register.as_view()),
    path("login/", UserLoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
