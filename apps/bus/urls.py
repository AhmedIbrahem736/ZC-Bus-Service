from django.urls import path
from .views import BusRouteListCreateAPIView, BusRouteRetrieveUpdateAPIView, BusRouteDeleteAPIView, BusStopListCreateAPIView, BusStopRetrieveUpdateAPIView, BusStopDeleteAPIView

urlpatterns = [
    path('bus-routes/', BusRouteListCreateAPIView.as_view(), name='bus-route-list-create'),
    path('bus-routes/<int:pk>/', BusRouteRetrieveUpdateAPIView.as_view(), name='bus-route-retrieve-update'),
    path('bus-routes/<int:pk>/delete/', BusRouteDeleteAPIView.as_view(), name='bus-route-delete'),
    path('bus-stops/', BusStopListCreateAPIView.as_view(), name='bus-stop-list-create'),
    path('bus-stops/<int:pk>/', BusStopRetrieveUpdateAPIView.as_view(), name='bus-stop-retrieve-update'),
    path('bus-stops/<int:pk>/delete/', BusStopDeleteAPIView.as_view(), name='bus-stop-delete'),
]
