from django.urls import path
from .views import BrowsingListings, UserListings, ListingDetail

urlpatterns = [
    path('', BrowsingListings.as_view()),
    path('user/', UserListings.as_view()),
    path('<slug:slug>/', ListingDetail.as_view()),
]