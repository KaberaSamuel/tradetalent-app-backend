from rest_framework import generics
from .models import Listing
from .serializers import ListingSerializer

class BrowsingListings(generics.ListCreateAPIView):
    queryset = Listing.objects.all() 
    serializer_class = ListingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
            # Filter out user listings
            return Listing.objects.exclude(user=self.request.user)

        
class UserListings(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_queryset(self):
            # Return only listings posted by user
            return Listing.objects.filter(user=self.request.user)


class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer