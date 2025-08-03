from django.urls import path
from api.views import UserListCreate, UserDetail, UserLoginView, Home, LogoutView

urlpatterns = [
    path("home/", Home.as_view()),
    path("users/", UserListCreate.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name ='logout')
]
