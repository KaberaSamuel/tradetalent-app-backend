from django.urls import path
from .views import UserListCreate, UserDetail, UserLoginView

urlpatterns = [
    path("users/", UserListCreate.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("login/", UserLoginView.as_view(), name="login")

]
