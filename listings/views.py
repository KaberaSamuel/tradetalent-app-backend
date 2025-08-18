from rest_framework import generics
from .models import Listing
from .serializers import ListingSerializer

class ListingListCreate(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def create(self, request, *args, **kwargs):
        # Adding user who is posting the listing
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)
    

class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer