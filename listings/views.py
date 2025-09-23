from .models import Listing
from .serializers import ListingSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView


class BrowsingListings(ListCreateAPIView):
    queryset = Listing.objects.all() 
    serializer_class = ListingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
       'title',
       'description',
       'skills'
   ]

    def get_queryset(self):
        # Filter out user listings
        queryset = Listing.objects.exclude(user=self.request.user)
        return queryset.order_by("-created_at")
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
class UserListings(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_queryset(self):
            # Return only listings posted by user
            return Listing.objects.filter(user=self.request.user)


class ListingDetail(RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = "slug"


class SearchListings(GenericAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
       queryset = self.filter_queryset(self.get_queryset())
       serializer = self.get_serializer(queryset, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    