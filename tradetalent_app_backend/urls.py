from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from . import routing


urlpatterns = [
    path("chats/", include("chat.urls")),
    path("ws/", include(routing.websocket_urlpatterns)),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", include("users.urls")),
    path("listings/", include("listings.urls")),
    path("admin/", admin.site.urls),
]
