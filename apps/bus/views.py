from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import BusRoute, BusStop, BusSubscription, BusReservation
from .serializers import BusRouteSerializer, BusStopSerializer, BusSubscriptionSerializer, BusReservationSerializer


class BusRouteListCreateAPIView(generics.ListCreateAPIView):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = []
    
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
    

################################################################
################################ Bus Stop #####################

class BusStopListCreateAPIView(generics.ListCreateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('bus.add_busstop'):
            raise PermissionDenied("You do not have permission to create a bus stop.")
        
        return super().create(request, *args, **kwargs)


class BusStopRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.has_perm('bus.change_busstop'):
            raise PermissionDenied("You do not have permission to update this bus route.")
        return super().update(request, *args, **kwargs)
    

class BusStopDeleteAPIView(generics.DestroyAPIView):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm('bus.delete_busstop'):
            raise PermissionDenied("You do not have permission to delete this bus route.")
        return super().delete(request, *args, **kwargs)


class BusSubscriptionAPIView(generics.ListCreateAPIView):
    queryset = BusSubscription.objects.filter(is_safe_deleted=False)
    serializer_class = BusSubscriptionSerializer

    def get_queryset(self):
        if not self.request.user.has_perm('bus.view_bussubscription'):
            return self.queryset.filter(user=self.request.user)

        return self.queryset

    def get_serializer_context(self):
        return {'user': self.request.user}


class BusReservationAPIView(generics.ListCreateAPIView):
    queryset = BusReservation.objects.filter(is_safe_deleted=False)
    serializer_class = BusReservationSerializer

    def get_queryset(self):
        if not self.request.user.has_perm('bus.view_busreservation'):
            return BusReservation.objects.filter(is_safe_deleted=False, user=self.request.user)

        return BusReservation.objects.filter(is_safe_deleted=False)

    def get_serializer_context(self):
        return {'user': self.request.user}
