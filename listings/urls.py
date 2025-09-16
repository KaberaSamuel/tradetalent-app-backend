from django.urls import path
from .views import BrowsingListings, UserListings, ListingDetail, SearchListings

urlpatterns = [
    path('', BrowsingListings.as_view()),
    path('query/', SearchListings.as_view()),
    path('user/', UserListings.as_view()),
    path('<slug:slug>/', ListingDetail.as_view()),
]