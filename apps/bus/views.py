from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import BusRoute
from .serializers import BusRouteSerializer

class BusRouteListCreateAPIView(generics.ListCreateAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('bus.add_busroute'):
            raise PermissionDenied("You do not have permission to create a bus route.")
        
        return super().create(request, *args, **kwargs)
    

class BusRouteRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.has_perm('bus.change_busroute'):
            raise PermissionDenied("You do not have permission to update this bus route.")
        return super().update(request, *args, **kwargs)
    


class BusRouteDeleteAPIView(generics.DestroyAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm('bus.delete_busroute'):
            raise PermissionDenied("You do not have permission to delete this bus route.")
        return super().delete(request, *args, **kwargs)